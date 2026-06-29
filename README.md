# funeral-memorial-planning-agent-skill

> A compassionate, research-first Claude Skill that turns Claude into a funeral and memorial
> planning advisor versed in major religious and cultural rites, budgeting, and FTC
> consumer-protection rules. It screens for acute grief, scores the plan against world-renowned
> frameworks, and produces a prioritized, FTC-transparent improvement roadmap.

**Cluster:** Lifestyle & Personal (`lifestyle-personal`)  
**Skill slug:** `funeral-memorial-planning`  
**Source idea:** #112  
**Status:** Production-grade, all phases complete. Open-source (MIT).

---

## Table of Contents
1. [Why this exists](#why-this-exists)
2. [Key features](#key-features)
3. [How it works (harness flow)](#how-it-works-harness-flow)
4. [Scoring model](#scoring-model)
5. [Traditions supported](#traditions-supported)
6. [Safety: the hard gate](#safety-the-hard-gate)
7. [Repository layout](#repository-layout)
8. [Quick start](#quick-start)
9. [Using the knowledge updater](#using-the-knowledge-updater)
10. [Testing](#testing)
11. [Cross-skill integration](#cross-skill-integration)
12. [Safety, scope and disclaimers](#safety-scope-and-disclaimers)
13. [Roadmap](#roadmap)
14. [Contributing](#contributing)
15. [License](#license)
16. [Acknowledgements](#acknowledgements)

---

## Why this exists

Grieving families must plan funerals quickly - balancing religious and cultural customs,
dignity, legal and logistical steps, and budget - often while vulnerable to overcharging.
They are usually making irreversible decisions under emotional duress, sometimes within
hours of a loss.

`funeral-memorial-planning` addresses this by enforcing a **research-first harness** with an
explicit safety gate before any logistics are discussed, grounding every judgment in a
**named, citable framework**, and challenging its own conclusions (devil's advocate) before
presenting a professional artifact. It is not a chatbot that free-associates; it is a
reproducible, evidence-graded evaluation pipeline.

It is built for:
- Families and next-of-kin planning an at-need funeral.
- Individuals planning a pre-need (pre-death) funeral.
- Celebrants, hospice social workers, and faith leaders who need a structured reference.
- Open-source maintainers who want a citable, testable example of a safety-gated Claude Skill.

## Key features

- **Hard safety gate first.** Acute grief, suicidal ideation, coercion, and acute traumatic
  loss are screened before any scores, plans, or vendor logistics are produced.
- **Multi-religion rite sequencing.** Culturally-correct sequences for Catholic, Protestant,
  Muslim, Jewish, Hindu, Buddhist, and secular traditions - not generic templates.
- **FTC Funeral Rule compliance.** Itemized General Price List breakdown, embalming opt-out,
  outer-burial-container disclosure, third-party casket right, itemized Statement of Goods
  and Services. No bundled "package" prices are accepted without breakdown.
- **5-dimension, cited scoring (0-100).** Every sub-criterion cites a framework clause or an
  evidence source with an evidence tier.
- **Devil's-advocate quality gate.** A 7-point self-audit (rite audit, cost audit,
  emancipation audit, solemnity audit, safety re-check, citation audit) runs before output.
- **Self-improving knowledge base.** A resilient crawl4ai pipeline (`tools/knowledge_updater.py`)
  grows `SECOND-KNOWLEDGE-BRAIN.md` weekly with de-duplicated, scored, dated entries.
- **Offline-testable.** 22 pytest tests run with zero network access.

## How it works (harness flow)

```
/funeral-memorial-planning   (skills/main.md)
   |
   v
[1] sub-profile-intake        -> structured intake payload
   |                              (tradition, budget, timeline, disposition, emotional state)
   v
[2] HARD GATE: sub-safety-screener   -> pass | caution | block
   |                                     (BLOCKS the harness on acute crisis / coercion)
   v
[3] research (WebSearch / WebFetch)   -> evidence
   |                                     (fallback: SECOND-KNOWLEDGE-BRAIN.md, confidence cap 0.6)
   v
[4] sub-scoring-engine               -> 0-100 across 5 cited dimensions
   |
   v
[5] sub-improvement-roadmap           -> effort x impact roadmap
   |                                     (FTC-itemized, culturally-sequenced rites)
   v
[6] devil's-advocate quality gate     -> final professional artifact
```

Stages run in strict order. No stage may execute before its precondition is met. If the safety
gate returns `block`, stages 3-6 are never run.

## Scoring model

Each dimension is scored 0-100 as the sum of weighted sub-criteria. Every sub-criterion carries
a citation and an evidence tier.

| Dimension | Weight | Framework |
|-----------|-------|-----------|
| Solemnity / Appropriateness | 0.20 | Stroebe and Schut Dual Process Model (1999) |
| Rite completeness | 0.25 | Major-tradition rites canon |
| Logistics readiness | 0.20 | Event-logistics critical-path planning |
| Budget fit | 0.20 | FTC Funeral Rule (16 CFR Part 453) + NFDA median benchmarks |
| Consumer protection | 0.15 | FTC Funeral Rule (16 CFR Part 453) |

```
composite = 100 * (w1*d1 + w2*d2 + w3*d3 + w4*d4 + w5*d5)
weights = [0.20, 0.25, 0.20, 0.20, 0.15]   # sum = 1.0
```

Weights are always surfaced to the user. Re-weighting is allowed per case but must be stated
with rationale and must preserve sum(weights) = 1.0. When only the knowledge-base fallback is
used, the affected dimension's confidence is capped at 0.6.

Evidence hierarchy enforced: Systematic Review > Meta-Analysis > RCT/Empirical > Cohort >
Expert Opinion > Knowledge-Base fallback.

## Traditions supported

| Tradition | Required-rite checklist (completeness) |
|-----------|----------------------------------------|
| Catholic | Vigil/Wake, Funeral Mass or Liturgy of the Word, Rite of Committal |
| Protestant | Service, scripture/music, committal |
| Muslim | Ghusl, Kafan, Janazah prayer, Dafan (burial within 24h) |
| Jewish | Shmira, Taharah, Tachrichim, Levayah, Kevurah, Shiva |
| Hindu | Preparation, cremation within 24h, Antyeshti, 13-day Sutak, Shraddha |
| Buddhist | Chanting/merit transfer, wake, 7th-day and 49th-day observance |
| Secular | Gathering, eulogy/celebration of life, committal or symbolic act |

Each tradition also drives intake-specific questions (e.g., Chevra Kadisha contact for Jewish,
Janazah committee for Muslim, Requiem vs. standard Mass for Catholic).

## Safety: the hard gate

`sub-safety-screener` runs immediately after intake and MUST pass before any guidance is
emitted. It is conservative - when in doubt, it trips.

Blocking classes (HARD STOP if any is true):
- **A. Acute crisis / suicidal ideation** - self-harm intent patterns, or hopelessness paired
  with plan/means (pills, gun, rope, bridge, overdose), or explicit `crisis` emotional state.
- **B. Vulnerable person / coercion** - minor or under guardianship, coercion by a funeral
  home or family ("won't give me the GPL", "forced to sign"), or signs of incapacity.
- **C. Acute traumatic loss** - death within 0-72 hours AND acute/crisis state, or death by
  homicide, suicide of the deceased, or mass-casualty event.

When `block` trips, the harness STOPS and emits verified crisis resources:

- 988 Suicide and Crisis Lifeline (US): call or text 988
- SAMHSA National Helpline (US): 1-800-662-4357
- Crisis Text Line: text HOME to 741741
- Veterans Crisis Line: dial 988 then press 1
- International: IASP crisis-centre directory (https://www.iasp.info/resources/Crisis_Centres/)

## Repository layout

```
funeral-memorial-planning-agent-skill/
|-- skills/
|   |-- main.md                      Harness: stages, quality gates, devil's advocate
|   |-- sub-profile-intake.md        Intake schema + tradition-specific addenda
|   |-- sub-safety-screener.md       HARD GATE: blocking classes A/B/C + referrals
|   |-- sub-scoring-engine.md        5-dimension rubric, weights, evidence tiers
|   `-- sub-improvement-roadmap.md   Rite sequencing + FTC itemized cost template
|-- tools/
|   `-- knowledge_updater.py         crawl4ai pipeline: fetch, parse, score, dedup, append
|-- tests/
|   |-- test-scenarios.md            7 end-to-end + regression scenarios
|   `-- test_knowledge_updater.py    22 offline pytest tests (no network)
|-- SECOND-KNOWLEDGE-BRAIN.md        Living knowledge base (15 seeded authorities)
|-- INTEGRATION.md                   Cross-skill wiring + scoring-scale contract
|-- CLAUDE.md                        Skill identity and active tasks
|-- PROJECT-detail.md                Full technical spec
|-- PROJECT-DEVELOPMENT-PHASE-TRACKING.md   Phase roadmap (all DONE)
|-- README.md                        This file
|-- LICENSE                          MIT
`-- requirements.txt                 Python deps (crawl4ai, pytest)
```

## Quick start

The skill itself is Markdown - no installation is needed to use it as a Claude Skill. Copy the
`skills/` directory into your Claude Skills directory and invoke `/funeral-memorial-planning`.

For the weekly knowledge-base refresh, install the optional Python dependencies:

```bash
pip install -r requirements.txt
```

Then, to run the skill end-to-end, invoke it in Claude and answer the intake questions. The
harness will: collect intake, run the hard gate, gather evidence, score, build a roadmap, and
run the devil's-advocate gate before emitting the artifact.

## Using the knowledge updater

`tools/knowledge_updater.py` is the self-improving knowledge pipeline. It is resilient: one
failed source does not abort the run.

```bash
# Live crawl + append (requires crawl4ai and network)
python tools/knowledge_updater.py

# Score only, print JSON, do not write
python tools/knowledge_updater.py --dry-run

# Register curated seed entries per source without any network
python tools/knowledge_updater.py --offline-seed

# Filter and cap
python tools/knowledge_updater.py --since 2026-01-01 --limit 20 --sources ftc,gbc

# Point at a different knowledge-base file
python tools/knowledge_updater.py --brain path/to/SECOND-KNOWLEDGE-BRAIN.md

# Verbose logging
python tools/knowledge_updater.py -v
```

Recommended weekly cron (Linux/macOS):

```
0 3 * * 1  cd /path/to/funeral-memorial-planning-agent-skill && python tools/knowledge_updater.py
```

Pipeline: fetch (crawl4ai) -> parse (title, abstract, year, URL) -> score (recency + domain
relevance) -> dedup (sha256 of URL/title, first 16 hex chars) -> append (dated, structured
entries to `SECOND-KNOWLEDGE-BRAIN.md`).

## Testing

```bash
# 22 offline unit tests - no network required
python -m pytest tests -q

# Smoke test the knowledge updater
python tools/knowledge_updater.py --dry-run --offline-seed --limit 1
```

The test suite covers: entry hashing stability, page parsing (title/abstract extraction and
fallbacks), scoring (unit interval, recency decay), de-duplication (hash-tag reading, duplicate
and empty-identity skips), append block format, source selection, date filtering, the offline
seed builder, and the full CLI (dry-run, append, invalid input).

## Cross-skill integration

`funeral-memorial-planning` is a member of the `lifestyle-personal` cluster. `INTEGRATION.md`
defines the contract for sharing sub-skills with siblings (wedding-planning,
end-of-life-advance-directives, personal-finance-budgeting, event-coordination) without
divergence:

- A shared 0-100 scoring scale with common banding (90-100 exemplary, 75-89 solid, 60-74 gaps,
  40-59 weak, 0-39 failing).
- Weights always sum to 1.0 and are surfaced with rationale.
- The hard gate is the cluster's canonical crisis screen (single source of truth for crisis
  resources).
- Sibling skills may read `SECOND-KNOWLEDGE-BRAIN.md` and append their own dated crawl sections
  but never edit another skill's entries.
- Schema changes to shared sub-skills are breaking changes and are recorded in the changelog in
  `INTEGRATION.md`.

## Safety, scope and disclaimers

This skill is **not** a funeral director, attorney, therapist, or member of the clergy. It
defers to licensed professionals and says so explicitly. Specifically, it will:

- Refuse to recommend specific vendors for a fee; it provides vetting criteria instead.
- Refuse to override documented pre-need instructions of the deceased.
- Refuse to provide legal, tax, or medical advice; it refers to licensed professionals.
- Refuse to proceed with logistics if the safety gate blocks; it offers bereavement support only.

Crisis resources emitted by the gate are US-centric by default, with the IASP international
directory linked for non-US users. Before deploying in a new jurisdiction, review the
jurisdictional accuracy of crisis numbers and disposition statutes.

## Roadmap

- First live network crawl validation against FTC, NFDA, and GBC pages.
- Expand the source registry with additional regional funeral-rule authorities.
- Add non-US consumer-protection frameworks (e.g., UK Funeral Market Investigation Order).
- Add localized crisis-resource packs per jurisdiction.
- Add a JSON-schema validator for sub-skill payloads.

## Contributing

Contributions are welcome. Please:

1. Open an issue describing the change.
2. Ensure `python -m pytest tests -q` passes (22 tests, no network).
3. Keep all citations real and verifiable - do not invent sources.
4. Preserve the hard-gate contract: the safety gate must run before any logistics.
5. Document any shared-sub-skill schema change in the `INTEGRATION.md` changelog.

## License

MIT - see `LICENSE`. Underlying frameworks retain their respective licenses and citation
requirements: the FTC Funeral Rule (16 CFR Part 453), the National Funeral Directors Association,
the Green Burial Council, and the cited grief research (Kubler-Ross; Stroebe and Schut).

## Acknowledgements

- U.S. Federal Trade Commission - Funeral Rule (16 CFR Part 453).
- National Funeral Directors Association (NFDA) - statistics and code of conduct.
- Green Burial Council (GBC) - natural-burial standards.
- Cremation Association of North America (CANA).
- Hospice Foundation of America - grief and loss resources.
- Elisabeth Kubler-Ross - grief-stage model (1969).
- Margaret Stroebe and Henk Schut - Dual Process Model of coping with bereavement (1999).
- U.S. Conference of Catholic Bishops - Order of Christian Funerals.
- Islamic Society of North America, Kavod v'Nichum, Hindu American Foundation, and Buddhist
  Churches of America - tradition-specific rite guidance.

---

Made with care for families navigating loss.
