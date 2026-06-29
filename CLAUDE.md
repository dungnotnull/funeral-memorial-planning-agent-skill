# CLAUDE.md - Funeral / Memorial Planning Support (custom & religion) (idea 112)

## Skill Identity
- **Name / slug:** `funeral-memorial-planning`
- **Tagline:** Funeral / Memorial Planning Support (custom & religion)
- **Source idea:** #112 (`ideas.md`)
- **Cluster:** Lifestyle & Personal (`lifestyle-personal`)
- **Current phase:** Phase 5 - Integration & Cross-Skill Wiring COMPLETE (all phases done).

## Problem This Skill Solves
Grieving families must plan funerals quickly, balancing religious/cultural customs, dignity,
legal/logistical steps, and budget - often while vulnerable to overcharging.

This skill becomes **a compassionate funeral and memorial planning advisor versed in major
religious and cultural rites, budgeting, and consumer-protection rules**. It is research-first,
grounds every score in named world-renowned frameworks, challenges its own assumptions before
concluding, and produces a professional artifact: a multi-dimensional score plus a prioritized
improvement roadmap.

## Harness Flow Summary
1. **Intake** -> `sub-profile-intake` gathers structured inputs.
2. **HARD GATE** -> `sub-safety-screener` runs before anything else; blocks on acute grief /
   suicidal ideation / coercion / acute traumatic loss.
3. **Research** -> WebSearch/WebFetch enrich evidence (graceful degradation to
   `SECOND-KNOWLEDGE-BRAIN.md`, confidence cap 0.6).
4. **Scoring** -> `sub-scoring-engine` produces 0-100 across 5 cited dimensions.
5. **Roadmap** -> `sub-improvement-roadmap`: effort x impact, FTC-itemized, culturally-sequenced.
6. **Quality gate** -> devil's-advocate review (rite audit, cost audit, emancipation audit,
   solemnity audit, safety re-check, citation audit) before final output.

**SAFETY GATE:** `sub-safety-screener` MUST pass before any guidance is emitted.

## Sub-skills
- `skills/sub-profile-intake.md` - intake schema + tradition-specific addenda.
- `skills/sub-safety-screener.md` - HARD GATE: blocking classes A/B/C + referral resources.
- `skills/sub-scoring-engine.md` - 5-dimension rubric, weights, evidence tiers.
- `skills/sub-improvement-roadmap.md` - rite sequencing + FTC itemized cost template.

## Tools Required
- `WebSearch`, `WebFetch` - live evidence gathering
- `Read`, `Write` - artifact production
- `python` - run `tools/knowledge_updater.py`

## Knowledge Sources (crawl targets)
- FTC Funeral Rule guidance (16 CFR Part 453)
- National Funeral Directors Association (NFDA)
- Religious authority guides on rites
- Green Burial Council standards
- Cremation Association of North America; Hospice Foundation grief resources.

## Supporting Tools
- `tools/knowledge_updater.py` - crawl4ai pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md`
  (weekly cron recommended). CLI: `--dry-run`, `--since`, `--limit`, `--sources`,
  `--offline-seed`, `--brain`. Resilient: one failed source does not abort the run.

## Testing
- `python -m pytest tests -q` - 22 offline unit tests (no network).
- `tests/test-scenarios.md` - 7 end-to-end + regression scenarios.

## Active Development Tasks
- [x] Scaffold all required deliverables
- [x] Author main harness + 4 sub-skills (production-grade, domain-specific)
- [x] Define scoring dimensions: Solemnity/Appropriateness, Rite completeness, Logistics readiness, Budget fit, Consumer protection
- [x] SECOND-KNOWLEDGE-BRAIN seeded with 15 verified authorities; `knowledge_updater.py` production-ready for live crawl
- [x] 7 regression scenarios + 22 offline pytest tests
- [x] Cross-skill wiring contract (`INTEGRATION.md`) + open-source packaging (README, LICENSE, requirements.txt)

## Related Root Docs
- `PROJECT-detail.md` - full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - phase roadmap (all phases DONE)
- `SECOND-KNOWLEDGE-BRAIN.md` - living knowledge base
- `INTEGRATION.md` - cross-skill wiring contract
- `README.md` - open-source readme
