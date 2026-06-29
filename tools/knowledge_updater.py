# -*- coding: utf-8 -*-
"""knowledge_updater.py - SECOND-KNOWLEDGE-BRAIN crawler for `funeral-memorial-planning`.

Production pipeline:
  1. fetch      - retrieve each registered authoritative source URL with crawl4ai
  2. parse      - extract title, summary, published date, url from raw page text/markdown
  3. score      - recency + domain-keyword relevance in [0, 1]
  4. dedup      - skip entries whose URL/title hash is already in the brain
  5. append     - write dated, structured entries to SECOND-KNOWLEDGE-BRAIN.md
  6. summarize  - print a per-source success/failure report

The crawler is resilient: if crawl4ai is not installed or a fetch fails, it logs a
warning and continues with the remaining sources. It never raises on a single source
failure. Network access is only needed for the live fetch path; all parsing, scoring,
dedup and append logic is pure-Python and fully unit-testable offline.

Usage:
    python tools/knowledge_updater.py                  # live crawl + append
    python tools/knowledge_updater.py --dry-run         # score only, print JSON, no write
    python tools/knowledge_updater.py --since 2026-01-01 --limit 20
    python tools/knowledge_updater.py --brain path/to/SECOND-KNOWLEDGE-BRAIN.md
    python tools/knowledge_updater.py --sources ftc,nfda
"""
from __future__ import annotations

import argparse
import asyncio
import datetime as _dt
import hashlib
import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import Iterable

LOG = logging.getLogger("knowledge_updater")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BRAIN = os.path.join(HERE, "..", "SECOND-KNOWLEDGE-BRAIN.md")

DOMAIN_KEYWORDS: tuple[str, ...] = (
    "funeral", "memorial", "bereavement", "grief", "cremation", "burial",
    "green burial", "funeral rule", "itemized", "general price list",
    "janazah", "taharah", "shiva", "antyeshti", "vigil", "committal",
    "solemnity", "rite", "consumer protection", "embalming",
)

# Each registered source is a real, citable authority. `query` is appended to the
# fetched URL only where the source exposes a search endpoint; otherwise the
# canonical page is fetched directly and parsed in full.
@dataclass(frozen=True)
class Source:
    key: str
    name: str
    url: str
    category: str
    search: bool = False  # True if url is a search endpoint expecting ?q=

SOURCES: tuple[Source, ...] = (
    Source("ftc_rule", "FTC Funeral Rule (16 CFR Part 453)",
           "https://www.ftc.gov/legal-library/browse/rules/funeral-rule",
           "consumer_protection"),
    Source("ftc_consumer", "FTC Consumer Guidance - Funerals",
           "https://consumer.ftc.gov/articles/0300-ftc-funeral-rule",
           "consumer_protection"),
    Source("nfda_stats", "National Funeral Directors Association - Statistics",
           "https://www.nfda.org/news/statistics", "cost_benchmark"),
    Source("nfda_ethics", "NFDA Code of Professional Conduct",
           "https://www.nfda.org/about/code-of-professional-conduct",
           "consumer_protection"),
    Source("gbc_standards", "Green Burial Council - Standards",
           "https://www.greenburialcouncil.org/our_standards.html",
           "green_burial"),
    Source("gbc_home", "Green Burial Council - Home",
           "https://www.greenburialcouncil.org/", "green_burial"),
    Source("cana", "Cremation Association of North America",
           "https://www.cremationassociation.org/", "cremation"),
    Source("nfda_grief", "NFDA - Grief Resources",
           "https://www.nfda.org/grief-support.html", "grief"),
    Source("hospice_grief", "Hospice Foundation - Grief & Loss",
           "https://hospicefoundation.org/grief-and-loss/", "grief"),
)

SEARCH_QUERIES: tuple[str, ...] = (
    "funeral cost transparency consumer protection",
    "green burial standards update",
    "religious funeral rites guidelines",
    "grief support evidence based",
)

ENTRY_DATE_RE = re.compile(r"\b(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")
TITLE_TAG_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
HEADING_RE = re.compile(r"^\s{0,3}#{1,3}\s+(.+?)\s*$", re.MULTILINE)
HASH_TAG_RE = re.compile(r"<!--hash:([0-9a-f]{16})-->")


@dataclass
class Entry:
    title: str
    authors: str
    year: int
    venue: str
    url: str
    abstract: str
    category: str
    source_key: str
    fetched_at: str = field(default_factory=lambda: _dt.date.today().isoformat())

    def hash(self) -> str:
        basis = (self.url or self.title or "").strip().lower()
        return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict:
        return asdict(self)


def _normalize(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_page(raw: str, source: Source) -> Entry:
    """Extract a structured Entry from raw page HTML/markdown text."""
    raw = raw or ""
    m = TITLE_TAG_RE.search(raw)
    title = _normalize(m.group(1)) if m else ""
    if not title:
        hm = HEADING_RE.search(raw)
        title = _normalize(hm.group(1)) if hm else source.name

    md = re.sub(r"<[^>]+>", " ", raw)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", md) if p.strip()]
    abstract = ""
    for p in paragraphs:
        clean = _normalize(p)
        if len(clean) >= 60 and not clean.lower().startswith(("cookie", "skip to", "menu")):
            abstract = clean[:500]
            break
    if not abstract:
        abstract = _normalize(md)[:500]

    dm = ENTRY_DATE_RE.search(raw)
    year = int(dm.group(1)) if dm else _dt.date.today().year
    return Entry(
        title=title[:240],
        authors="",
        year=year,
        venue=source.name,
        url=source.url,
        abstract=abstract,
        category=source.category,
        source_key=source.key,
    )


def score_entry(entry: Entry) -> float:
    """Recency + relevance score in [0, 1]."""
    now = _dt.date.today().year
    if entry.year and 1900 <= entry.year <= now + 1:
        recency = max(0.0, 1.0 - (now - entry.year) / 10.0)
    else:
        recency = 0.3
    text = (entry.title + " " + entry.abstract + " " + entry.category).lower()
    hits = sum(1 for k in DOMAIN_KEYWORDS if k in text)
    relevance = min(1.0, hits / 6.0)
    return round(0.5 * recency + 0.5 * relevance, 3)


def load_existing_hashes(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(HASH_TAG_RE.findall(f.read()))


def filter_since(entries: Iterable[Entry], since: _dt.date | None) -> list[Entry]:
    if since is None:
        return list(entries)
    out: list[Entry] = []
    for e in entries:
        try:
            d = _dt.date.fromisoformat(e.fetched_at)
        except ValueError:
            continue
        if d >= since:
            out.append(e)
    return out


def format_entry(entry: Entry, score: float) -> str:
    return (
        f"- {entry.fetched_at} | score={score} | **{entry.title}** "
        f"| {entry.authors or '-'} | {entry.year} | {entry.venue} "
        f"| {entry.category} | {entry.url} "
        f"| key={entry.source_key} <!--hash:{entry.hash()}-->"
    )


def append_entries(entries: list[Entry], path: str) -> int:
    existing = load_existing_hashes(path)
    today = _dt.date.today().isoformat()
    lines: list[str] = []
    added = 0
    for e in sorted(entries, key=score_entry, reverse=True):
        h = e.hash()
        if h in existing or not (e.url or e.title):
            continue
        existing.add(h)
        lines.append(format_entry(e, score_entry(e)))
        added += 1
    if not added:
        LOG.info("no new entries to append")
        return 0
    block = f"\n### Crawl {today} (+{added})\n" + "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(block)
    LOG.info("appended %d new entries to %s", added, path)
    return added


async def fetch_source(crawler, source: Source) -> Entry | None:
    try:
        res = await crawler.arun(url=source.url)
    except Exception as exc:  # network/runtime failure of one source must not abort the run
        LOG.warning("fetch failed for %s (%s): %s", source.key, source.url, exc)
        return None
    raw = getattr(res, "markdown", None) or getattr(res, "html", None) or ""
    if not raw:
        LOG.warning("empty body for %s", source.key)
        return None
    return parse_page(raw, source)


async def crawl(sources: list[Source]) -> list[Entry]:
    entries: list[Entry] = []
    try:
        from crawl4ai import AsyncWebCrawler
    except ImportError:
        LOG.warning("crawl4ai not installed; live crawl skipped. Install with: pip install crawl4ai")
        return entries
    async with AsyncWebCrawler(verbose=False) as crawler:
        for source in sources:
            entry = await fetch_source(crawler, source)
            if entry is not None:
                entries.append(entry)
                LOG.info("fetched %s: %s", source.key, entry.title[:80])
    return entries


def select_sources(keys: list[str] | None) -> list[Source]:
    if not keys:
        return list(SOURCES)
    keyset = {k.strip().lower() for k in keys}
    return [s for s in SOURCES if s.key.lower() in keyset]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Refresh SECOND-KNOWLEDGE-BRAIN.md")
    ap.add_argument("--brain", default=DEFAULT_BRAIN, help="path to the knowledge-base markdown")
    ap.add_argument("--dry-run", action="store_true", help="score and print only; do not write")
    ap.add_argument("--since", help="only keep entries fetched on/after YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=0, help="cap number of appended entries (0 = no cap)")
    ap.add_argument("--sources", help="comma-separated source keys to crawl (default: all)")
    ap.add_argument("--offline-seed", action="store_true",
                    help="append a curated seed entry per source without any network access")
    ap.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    return ap.parse_args(argv)


def build_seed_entries(sources: list[Source]) -> list[Entry]:
    """Curated, offline entries derived from the source registry itself."""
    today = _dt.date.today().isoformat()
    return [
        Entry(
            title=s.name,
            authors=s.name.split(" - ")[0] if " - " in s.name else s.name,
            year=_dt.date.today().year,
            venue=s.name,
            url=s.url,
            abstract=f"Authoritative source registered for the {s.category} axis of the "
                    f"funeral-memorial-planning skill. Cite this page directly when its "
                    f"content is the basis for a scoring criterion.",
            category=s.category,
            source_key=s.key,
            fetched_at=today,
        )
        for s in sources
    ]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    sources = select_sources(args.sources.split(",") if args.sources else None)
    if not sources:
        LOG.error("no sources matched --sources=%s", args.sources)
        return 2

    if args.offline_seed:
        entries = build_seed_entries(sources)
    else:
        try:
            entries = asyncio.run(crawl(sources))
        except Exception as exc:
            LOG.error("crawl stage failed: %s", exc)
            entries = []

    since = None
    if args.since:
        try:
            since = _dt.date.fromisoformat(args.since)
        except ValueError:
            LOG.error("invalid --since date: %s", args.since)
            return 2
    entries = filter_since(entries, since)

    scored = [{**e.to_dict(), "hash": e.hash(), "score": score_entry(e)} for e in entries]
    if args.limit and len(scored) > args.limit:
        scored = sorted(scored, key=lambda d: d["score"], reverse=True)[: args.limit]
        entries = [e for e in entries if e.hash() in {d["hash"] for d in scored}]

    if args.dry_run:
        print(json.dumps(scored, indent=2, ensure_ascii=False))
        return 0

    if not entries and not args.offline_seed:
        LOG.warning("no live entries fetched; nothing to append. Try --offline-seed to register sources.")
        return 0

    added = append_entries(entries, args.brain)
    print(f"[ok] appended {added} new entries to {args.brain}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
