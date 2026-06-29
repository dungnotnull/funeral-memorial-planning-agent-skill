# -*- coding: utf-8 -*-
"""Offline unit tests for tools/knowledge_updater.py.

No network access required. Run with:
    python -m pytest tests/test_knowledge_updater.py -v
or:
    python tests/test_knowledge_updater.py
"""
import datetime as dt
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import knowledge_updater as ku  # noqa: E402


# --- Entry + hashing ----------------------------------------------------

def test_entry_hash_is_stable_and_16_hex():
    e = ku.Entry(title="T", authors="", year=2026, venue="V",
                 url="https://example.com/a", abstract="x",
                 category="consumer_protection", source_key="ftc_rule")
    h = e.hash()
    assert len(h) == 16
    int(h, 16)  # valid hex
    assert e.hash() == h  # stable


def test_entry_hash_ignores_url_casing_and_whitespace():
    a = ku.Entry("T", "", 2026, "V", "  HTTPS://Example.COM/A ", "x", "c", "k")
    b = ku.Entry("T", "", 2026, "V", "https://example.com/a", "x", "c", "k")
    assert a.hash() == b.hash()


# --- parse_page ---------------------------------------------------------

HTML_SAMPLE = """<!doctype html><html><head><title>FTC Funeral Rule</title></head>
<body><h1>Funeral Rule</h1>
<p>The Funeral Rule requires funeral homes to give consumers a General Price List.</p>
<nav>Skip to content</nav></body></html>"""


def test_parse_page_extracts_title_and_abstract():
    src = ku.SOURCES[0]
    e = ku.parse_page(HTML_SAMPLE, src)
    assert e.title == "FTC Funeral Rule"
    assert "General Price List" in e.abstract
    assert len(e.abstract) <= 500
    assert e.url == src.url
    assert e.source_key == src.key


def test_parse_page_falls_back_to_heading_when_no_title_tag():
    src = ku.SOURCES[0]
    e = ku.parse_page("# Heading One\n\nbody text here " + "x" * 80, src)
    assert e.title == "Heading One"


def test_parse_page_handles_empty_raw():
    src = ku.SOURCES[0]
    e = ku.parse_page("", src)
    assert e.title == src.name
    assert e.abstract == ""


# --- scoring -------------------------------------------------------------

def test_score_entry_in_unit_interval():
    e = ku.Entry("FTC Funeral Rule consumer protection itemized",
                 "", 2026, "FTC", "https://ftc.gov", "general price list embalming",
                 "consumer_protection", "ftc_rule")
    s = ku.score_entry(e)
    assert 0.0 <= s <= 1.0
    assert s > 0.5  # high keyword density + recent year


def test_score_entry_recency_decay_for_old_year():
    recent = ku.Entry("funeral rule", "", 2026, "FTC", "https://x", "funeral", "c", "k")
    old = ku.Entry("funeral rule", "", 2000, "FTC", "https://y", "funeral", "c", "k")
    assert ku.score_entry(recent) >= ku.score_entry(old)


def test_score_entry_zero_year_defaults_low_recency():
    e = ku.Entry("funeral", "", 0, "FTC", "https://x", "funeral", "c", "k")
    s = ku.score_entry(e)
    assert 0.0 <= s <= 1.0


# --- dedup + append -----------------------------------------------------

def _tmp_brain(tmp_path, content=""):
    p = tmp_path / "brain.md"
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_load_existing_hashes_reads_hash_tags(tmp_path):
    body = "### Crawl 2026-01-01\n- ... <!--hash:abcdef0123456789-->\n"
    p = _tmp_brain(tmp_path, body)
    hashes = ku.load_existing_hashes(p)
    assert "abcdef0123456789" in hashes


def test_load_existing_hashes_missing_file_returns_empty(tmp_path):
    assert ku.load_existing_hashes(str(tmp_path / "nope.md")) == set()


def test_append_entries_writes_block_and_returns_count(tmp_path):
    p = _tmp_brain(tmp_path, "")
    entries = [
        ku.Entry("Title A", "", 2026, "FTC", "https://a.example", "x", "c", "k1"),
        ku.Entry("Title B", "", 2026, "NFDA", "https://b.example", "y", "c", "k2"),
    ]
    added = ku.append_entries(entries, p)
    assert added == 2
    text = open(p, encoding="utf-8").read()
    assert "### Crawl " in text
    assert "Title A" in text and "Title B" in text
    assert "hash:" in text


def test_append_entries_skips_duplicates(tmp_path):
    p = _tmp_brain(tmp_path, "")
    e = ku.Entry("Title A", "", 2026, "FTC", "https://a.example", "x", "c", "k1")
    assert ku.append_entries([e], p) == 1
    assert ku.append_entries([e], p) == 0


def test_append_entries_skips_empty_identity(tmp_path):
    p = _tmp_brain(tmp_path, "")
    e = ku.Entry("", "", 2026, "", "", "x", "c", "k1")
    assert ku.append_entries([e], p) == 0


# --- filtering / selection ---------------------------------------------

def test_select_sources_all_when_none():
    assert len(ku.select_sources(None)) == len(ku.SOURCES)


def test_select_sources_subset_case_insensitive():
    sel = ku.select_sources(["FTC_RULE", "GBC_Standards"])
    assert [s.key for s in sel] == ["ftc_rule", "gbc_standards"]


def test_filter_since_keeps_recent(tmp_path):
    e_recent = ku.Entry("a", "", 2026, "v", "https://r", "x", "c", "k",
                        fetched_at="2026-06-29")
    e_old = ku.Entry("b", "", 2026, "v", "https://o", "x", "c", "k",
                     fetched_at="2020-01-01")
    kept = ku.filter_since([e_recent, e_old], dt.date(2026, 1, 1))
    assert kept == [e_recent]


def test_filter_since_none_returns_all():
    e = ku.Entry("a", "", 2026, "v", "https://r", "x", "c", "k")
    assert ku.filter_since([e], None) == [e]


# --- offline seed --------------------------------------------------------

def test_build_seed_entries_covers_sources():
    srcs = list(ku.SOURCES)[:3]
    seeds = ku.build_seed_entries(srcs)
    assert len(seeds) == 3
    assert {s.source_key for s in seeds} == {s.key for s in srcs}
    assert all(s.url for s in seeds)


# --- CLI dry-run --------------------------------------------------------

def test_dry_run_prints_json_and_writes_nothing(tmp_path, capsys):
    p = _tmp_brain(tmp_path, "")
    rc = ku.main(["--offline-seed", "--dry-run", "--brain", p, "--limit", "2"])
    out = capsys.readouterr().out
    assert rc == 0
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 2
    assert all("hash" in d and "score" in d for d in data)
    assert open(p, encoding="utf-8").read() == ""


def test_main_offline_seed_appends_to_brain(tmp_path):
    p = _tmp_brain(tmp_path, "")
    rc = ku.main(["--offline-seed", "--brain", p, "--limit", "1"])
    assert rc == 0
    assert "### Crawl" in open(p, encoding="utf-8").read()


def test_main_invalid_since_returns_2(tmp_path):
    p = _tmp_brain(tmp_path, "")
    rc = ku.main(["--offline-seed", "--since", "not-a-date", "--brain", p])
    assert rc == 2


def test_main_unknown_source_returns_2(tmp_path):
    p = _tmp_brain(tmp_path, "")
    rc = ku.main(["--sources", "nope", "--brain", p])
    assert rc == 2


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
