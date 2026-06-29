# PROJECT-detail.md - Funeral / Memorial Planning Support (custom & religion)

## Executive Summary
`funeral-memorial-planning` is a Claude Skill that turns Claude into **a compassionate funeral
and memorial planning advisor versed in major religious and cultural rites, budgeting, and
consumer-protection rules**. It ingests domain inputs, screens for safety/compliance, selects a
world-renowned evaluation framework, gathers fresh evidence, scores the subject across 5
dimensions, and outputs a prioritized improvement roadmap. It is part of the **Lifestyle &
Personal** cluster.

## Problem Statement
Grieving families must plan funerals quickly, balancing religious/cultural customs, dignity,
legal/logistical steps, and budget - often while vulnerable to overcharging.

Domain context: practitioners need reproducible, evidence-graded evaluation rather than ad-hoc
opinion. This skill enforces a research-first harness with explicit quality gates and a
self-improving knowledge base.

## Target Users and Use Cases
- Primary: practitioners, learners, and decision-makers in this domain.
- Trigger examples:
1. **Catholic funeral on a budget** - Family needs vigil/funeral Mass/rite of committal within
   a $6k budget. Expect rite sequencing, itemized cost guidance, FTC Funeral Rule rights.
2. **Buddhist 49-day observance** - User wants culturally correct sequence. Expect rite
   timeline and respectful logistics, not generic templates.
3. **Acute grief crisis** - User expresses hopelessness. Expect safety gate, bereavement
   hotline, before any vendor logistics.
4. **Green burial preference** - Eco-conscious family. Expect Green Burial Council standards
   and a provider-vetting roadmap.
5. **Overcharge protection** - Funeral home quoted a vague package. Expect FTC itemization
   rights and a negotiation/comparison checklist.

## Harness Architecture
```
/funeral-memorial-planning  (main.md)
   |
   v
[1] sub-profile-intake        -> structured intake
   |
   v
[2] GATE: sub-safety-screener  -> blocks unsafe/non-compliant requests
   |
   v
[3] research (WebSearch/WebFetch)        -> evidence (graceful deg: SECOND-KNOWLEDGE-BRAIN.md)
   |
   v
[4] scoring engine                       -> 0-100 multi-dimensional score
   |
   v
[5] improvement roadmap                  -> effort x impact prioritized actions
   |
   v
[6] quality-gate / devil's advocate      -> final professional artifact
```

## Full Sub-Skill Catalog

### `sub-profile-intake`
- **Purpose:** Capture tradition/religion, relationship to deceased, budget, timeline,
  body-disposition choice, and emotional state with sensitivity.
- **Inputs:** structured outputs from prior stage + user-supplied data.
- **Outputs:** validated, structured payload for the next stage.
- **Tools:** Read, Write.
- **Quality gate:** output schema validated before proceeding.

### `sub-safety-screener`
- **Purpose:** Detect acute grief crisis / suicidal ideation and surface bereavement support
  before planning logistics.
- **Inputs:** structured outputs from prior stage + user-supplied data.
- **Outputs:** validated, structured payload + a pass/refer verdict.
- **Tools:** Read, Write.
- **Quality gate:** BLOCKS the harness until satisfied (hard gate).

### `sub-scoring-engine`
- **Purpose:** Score the plan on solemnity/appropriateness, completeness of rites, logistics
  readiness, budget fit, and consumer protection.
- **Inputs:** structured outputs from prior stage + user-supplied data.
- **Outputs:** validated, structured payload for the next stage.
- **Tools:** Read, Write, WebSearch/WebFetch.
- **Quality gate:** output schema validated before proceeding.

### `sub-improvement-roadmap`
- **Purpose:** Produce a respectful checklist + timeline with cost transparency (FTC Funeral
  Rule) and culturally-correct rite sequencing.
- **Inputs:** structured outputs from prior stage + user-supplied data.
- **Outputs:** validated, structured payload for the next stage.
- **Tools:** Read, Write.
- **Quality gate:** output schema validated before proceeding.

## Evaluation Frameworks (world-renowned, citable)
- FTC Funeral Rule (consumer protection / itemized pricing)
- Major-tradition rites (Buddhist, Christian, Catholic, Muslim, Jewish, Hindu, secular)
- Bereavement and grief-stage models (Kubler-Ross, Dual Process Model)
- Event-logistics critical-path planning
- Green/natural burial standards (GBC)

## Scoring Model
| Dimension | Range | Notes |
|-----------|-------|-------|
| Solemnity/Appropriateness | 0-100 | Weighted contribution to the composite index |
| Rite completeness | 0-100 | Weighted contribution to the composite index |
| Logistics readiness | 0-100 | Weighted contribution to the composite index |
| Budget fit | 0-100 | Weighted contribution to the composite index |
| Consumer protection | 0-100 | Weighted contribution to the composite index |

Composite = weighted mean of dimensions (weights justified per case, surfaced to the user).
Every dimension score must cite at least one framework criterion or evidence source.

## Skill File Format Specification
Frontmatter: `name`, `description`. Required sections in `main.md`: Role and Persona, Workflow
(Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request; if inputs missing, run intake questions.
2. Run hard gate; if it fails, STOP and emit referral/disclaimer.
3. Gather evidence (prefer Systematic Review > Meta-analysis > RCT/empirical > expert opinion).
4. Score each dimension with cited justification.
5. Build prioritized roadmap.
6. Run devil's-advocate quality gate; revise; present artifact.
- Error handling: missing data -> state assumptions + confidence; tool failure -> degrade to
  knowledge base and signal limitation.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: FTC Funeral Rule guidance, National Funeral Directors Association (NFDA), Religious
  authority guides on rites, Green Burial Council standards.
- Crawl queries: funeral cost transparency consumer protection, green burial standards update,
  religious funeral rites guidelines, grief support evidence based.
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance.

## Supporting Tools Spec - `knowledge_updater.py`
- Inputs: source registry + query list (above), `--since` date.
- Outputs: appended, de-duplicated entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- Schedule: weekly cron.

## Quality Gates (must be true before final output)
- [ ] Hard safety/risk/compliance gate passed or referral issued
- [ ] Every score cites a framework criterion or evidence source
- [ ] Roadmap items have effort + impact + owner
- [ ] Assumptions and confidence stated; limitations disclosed
- [ ] Devil's-advocate pass completed

## Test Scenarios (at least 5)
1. **Catholic funeral on a budget** - Family needs vigil/funeral Mass/rite of committal within a
   $6k budget. Expect rite sequencing, itemized cost guidance, FTC Funeral Rule rights.
2. **Buddhist 49-day observance** - User wants culturally correct sequence. Expect rite timeline
   and respectful logistics, not generic templates.
3. **Acute grief crisis** - User expresses hopelessness. Expect safety gate, bereavement
   hotline, before any vendor logistics.
4. **Green burial preference** - Eco-conscious family. Expect Green Burial Council standards and
   a provider-vetting roadmap.
5. **Overcharge protection** - Funeral home quoted a vague package. Expect FTC itemization rights
   and a negotiation/comparison checklist.

## Key Design Decisions
1. Research-first; no memory-only claims when search is possible.
2. Named frameworks only - never ad hoc criteria.
3. Hard gate precedes all guidance for this safety/compliance-sensitive domain.
4. Multi-dimensional score + prioritized roadmap are mandatory outputs.
5. Self-improving knowledge base via weekly crawl.
