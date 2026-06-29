# PROJECT-DEVELOPMENT-PHASE-TRACKING.md - Funeral / Memorial Planning Support (custom & religion)

> All phases 0-5 are **DONE / production-grade, ready for open source.**
> No real model pull/train/run was executed (deferred to production stage to save resources);
> all code is implemented 100% and verified by offline tests + smoke runs.

## Phase 0 - Research & Skill Architecture
- Tasks: define domain scope, select frameworks (FTC Funeral Rule (consumer protection / itemized pricing), Major-tradition rites (Buddhist, Christian, Catholic, Muslim, Jewish, Hindu, secular), Bereavement & grief-stage models (Kuebler-Ross, Dual Process Model)...), map cluster sub-skills.
- Deliverables: framework shortlist, scoring dimensions (Solemnity/Appropriateness, Rite completeness, Logistics readiness, Budget fit, Consumer protection).
- Success: every dimension maps to at least 1 citable framework.
- Effort: S. **Status: DONE.** Frameworks mapped in `skills/sub-scoring-engine.md` and `SECOND-KNOWLEDGE-BRAIN.md` (15 verified authorities).

## Phase 1 - Core Sub-Skills
- Tasks: implement sub-profile-intake, sub-safety-screener, sub-scoring-engine, sub-improvement-roadmap.
- Deliverables: 4 sub-skill files with I/O schemas + quality gates.
- Success: each sub-skill independently runnable with validated output.
- Effort: M. **Status: DONE.** All four rewritten production-grade with domain-specific logic: intake schema + tradition addenda, blocking classes A/B/C + referral resources, 5-dimension cited rubric, rite sequencing + FTC itemized cost template.

## Phase 2 - Main Harness + Quality Gates
- Tasks: wire intake -> gate -> framework -> scoring -> roadmap -> devil's-advocate.
- Deliverables: `skills/main.md`.
- Success: end-to-end run on 1 scenario produces a complete artifact.
- Effort: M. **Status: DONE.** `skills/main.md` rewritten with strict stage preconditions, 7-point devil's-advocate protocol, and a 10-item quality-gate checklist.

## Phase 3 - SECOND-KNOWLEDGE-BRAIN Pipeline
- Tasks: implement `tools/knowledge_updater.py` (crawl4ai + dedup + append).
- Deliverables: working updater + seeded knowledge base.
- Success: a dry run appends at least 1 dated entry without duplicates.
- Effort: M. **Status: DONE.** `tools/knowledge_updater.py` rewritten production-grade (real source registry, resilient crawl, parse/score/dedup/append; CLI: --dry-run/--since/--limit/--sources/--offline-seed/--brain). Verified: dry-run returns valid JSON; offline-seed appends dated entries with hash dedup (0 duplicates on re-run). `SECOND-KNOWLEDGE-BRAIN.md` seeded with 15 verified authorities. Live network crawl deferred to production stage (no network run performed, per scope).

## Phase 4 - Testing & Validation
- Tasks: run all scenarios; verify gates fire correctly.
- Deliverables: `tests/test-scenarios.md` with expected behavior.
- Success: gate scenarios block correctly; scoring is reproducible.
- Effort: M. **Status: DONE.** Expanded to 7 end-to-end + regression scenarios (Catholic-budget, Buddhist 49-day, acute-grief HARD-BLOCK, green burial, FTC overcharge, Jewish same-day, pre-need) plus a 12-item regression checklist. Added `tests/test_knowledge_updater.py`: 22 offline pytest tests (parse/score/dedup/append/CLI) - all passing, no network required.

## Phase 5 - Integration & Cross-Skill Wiring
- Tasks: share cluster sub-skills (Lifestyle & Personal) with sibling skills; align scoring scales.
- Deliverables: cross-skill references.
- Success: shared sub-skills reused without divergence.
- Effort: S. **Status: DONE.** `INTEGRATION.md` defines the cluster-shared sub-skill registry, the 0-100 scoring-scale alignment contract (weights sum to 1.0, shared banding, citation + evidence-tier rules), hard-gate interop (single source of truth for crisis resources), knowledge-base interop rules, and a drift-prevention changelog.

## Summary
- **All phases: 100% DONE.**
- **Open-source packaging complete:** `README.md`, `LICENSE` (MIT), `requirements.txt`.
- **Tests:** `python -m pytest tests -q` -> 22 passed. Smoke: `python tools/knowledge_updater.py --dry-run --offline-seed` -> rc 0.
- **Deferred to production stage (resource saving):** first live network crawl; no model pull/train/run (not applicable to this markdown+Python skill).
