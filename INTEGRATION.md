# INTEGRATION.md - Cross-Skill Wiring (Phase 5)

`funeral-memorial-planning` is a member of the **Lifestyle & Personal** skill cluster
(`lifestyle-personal`). This document defines how it shares sub-skills and aligns scoring
scales with sibling skills in the cluster so that sub-skills are reused **without divergence**.

## 1. Cluster membership
- **Cluster:** `lifestyle-personal`
- **Sibling skills (referenced, not vendored):**
  - `wedding-planning` - event-logistics + budget critical-path planning shared.
  - `end-of-life-advance-directives` - bereavement/grief-stage models shared; safety-screener pattern reused.
  - `personal-finance-budgeting` - FTC-style itemized-cost template + budget-fit ratio reused.
  - `event-coordination` - critical-path planning + vendor-vetting checklist shared.
- **Canonical location of shared contracts:** `skills/cluster-shared.md` (this file's
  contract section below). Sibling skills MUST import (read) this contract rather than
  re-deriving scales, so revisions propagate without divergence.

## 2. Shared sub-skills (reused across the cluster)
The following sub-skills are designed to be cluster-shared. They expose a stable I/O schema
and are referenced by `funeral-memorial-planning` and the siblings above:

| Sub-skill | Owner | Reused by siblings for | Stable schema |
|-----------|-------|------------------------|---------------|
| `sub-safety-screener` | funeral-memorial-planning | acute-crisis / vulnerable-person hard gate | `verdict in {pass, caution, block}` + `matched_patterns` + `resources` |
| `sub-profile-intake` | funeral-memorial-planning | structured, sensitivity-first intake pattern | `intake_payload` with `assumptions`, `confidence` |
| `sub-scoring-engine` | funeral-memorial-planning | 0-100 multi-dimension cited scoring | `dimensions{}` + `composite` + `weights_used` |
| `sub-improvement-roadmap` | funeral-memorial-planning | effort x impact prioritized roadmap | `roadmap[]` with effort/impact/owner/cost_range/citation |

**Reuse rule:** a sibling skill consuming a shared sub-skill MUST preserve the sub-skill's
output schema verbatim and MUST NOT add cluster-specific fields inside the shared object.
Cluster-specific extensions go in a sibling-namespaced wrapper field (e.g.
`wedding_planning_extension: {...}`) so the shared payload stays canonical.

## 3. Cluster scoring-scale alignment contract
To keep scores comparable across the cluster, every sibling skill adheres to this contract:

- **Scale:** all dimension scores are 0-100, 1-decimal precision.
- **Composite:** weighted mean; weights sum to 1.0; weights + rationale are always surfaced.
- **Citations:** every dimension score cites a framework criterion or evidence source with an
  evidence tier; knowledge-base fallback caps confidence at 0.6.
- **Banding (shared interpretation):**
  - 90-100: exemplary / best-practice
  - 75-89: solid / actionable
  - 60-74: gaps present / needs roadmap
  - 40-59: weak / high-priority remediation
  - 0-39: failing / hard-stop review
- **Re-weighting:** allowed per-case but MUST be stated with rationale and MUST preserve
  sum(weights)=1.0.

## 4. Hard-gate interop
`sub-safety-screener` is the cluster's canonical HARD GATE. When a sibling skill detects a
domain crisis (e.g., advance-directives skill detects terminal-distress), it MUST delegate to
this gate's contract (same `verdict` enum, same referral resources) rather than implementing a
parallel one. This guarantees a single source of truth for crisis resources:
- 988 Suicide & Crisis Lifeline
- SAMHSA 1-800-662-4357
- Crisis Text Line (HOME to 741741)
- IASP crisis-centre directory https://www.iasp.info/resources/Crisis_Centres/

## 5. Knowledge-base interop
`SECOND-KNOWLEDGE-BRAIN.md` and `tools/knowledge_updater.py` are owned by this skill but are
designed to be referenced by sibling skills via read-only access. Sibling skills append their
own dated crawl sections under their own `### Crawl YYYY-MM-DD (+N)` headers (never edit
another skill's entries). The dedup hash is sha256(url/title)[:16], shared across the cluster.

## 6. Drift prevention
- Any change to a shared sub-skill's output schema is a **breaking change** and MUST be
  documented in this file's changelog below with the date and affected siblings.
- The regression checklist in `tests/test-scenarios.md` MUST pass for every shared sub-skill
  before a change is merged.

### Changelog
- 2026-06-29: Initial cross-skill wiring contract established (Phase 5). Defined shared
  sub-skills, scoring-scale alignment, hard-gate interop, and knowledge-base interop.
