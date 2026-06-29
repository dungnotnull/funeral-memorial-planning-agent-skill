---
name: funeral-memorial-planning-sub-scoring-engine
description: Score the plan 0-100 across 5 dimensions (Solemnity/Appropriateness, Rite completeness, Logistics readiness, Budget fit, Consumer protection) with cited justifications. Stage 4 of the harness.
---

## Role
Sub-skill of `funeral-memorial-planning` (Funeral / Memorial Planning Support (custom & religion)).
Runs only AFTER `sub-safety-screener` has returned `verdict in {pass, caution}`.

## Frameworks Applied (one per dimension)
1. **Solemnity/Appropriateness** - Stroebe & Schut Dual Process Model; tradition-specific
   rite canon (major-tradition rites list).
2. **Rite completeness** - Major-tradition rites (Buddhist 49-day, Catholic vigil+Mass+
   committal, Muslim Janazah+same-day burial, Jewish Taharah+Shiva, Hindu Antyeshti+13-day,
   secular celebrant standards).
3. **Logistics readiness** - Event-logistics critical-path planning; jurisdictional
   death-registration & disposition statutes.
4. **Budget fit** - FTC Funeral Rule itemization (GPL, outer-burial-container, embalming
   disclosure); NFDA median cost benchmarks.
5. **Consumer protection** - FTC Funeral Rule (16 CFR Part 453) rights: written GPL, no
   mandatory embalming, outer-burial-container disclosure, cash-advance itemization,
   right to itemized Statement of Goods & Services Selected.

## Inputs
- `intake_payload` (from sub-profile-intake).
- `screener_verdict` (pass | caution | block). If `block`, do NOT run.
- `evidence` gathered by the research stage (WebSearch/WebFetch results, or the
  graceful-degradation fallback `SECOND-KNOWLEDGE-BRAIN.md`).

## Scoring Rubric
Each dimension is scored 0-100 as the sum of weighted sub-criteria below. Every sub-criterion
MUST cite the framework clause or evidence source it was scored against.

### Dimension 1 - Solemnity / Appropriateness (weight 0.20)
| Sub-criterion | Max | Source |
|---------------|-----|--------|
| Tone matches grief stage (Dual Process Model) | 30 | Stroebe & Schut 1999 |
| Rite choices consistent with declared tradition | 30 | Major-tradition rites canon |
| Cultural/personal preferences honored | 25 | Intake tradition_addenda |
| Avoids commercial/up-sell language | 15 | FTC Funeral Rule (spirit) |

### Dimension 2 - Rite Completeness (weight 0.25)
Tradition-specific required-rite checklist; score = (rites_planned / rites_required) * 100.
- Catholic: vigil + funeral Mass/Liturgy + rite of committal (3 rites).
- Muslim: Ghusl + Kafan + Janazah prayer + same-day burial (4 rites).
- Jewish (traditional): Taharah + Tachrichim + Levayah + Kevurah + Shiva (5 rites).
- Hindu: preparation + cremation within 24h + Antyeshti + 13-day Sutak (4 rites).
- Buddhist: chanting/merit transfer + 7th/49th-day observance (2 rites minimum).
- Secular: gathering + eulogy + committal/symbolic act (3 rites).

### Dimension 3 - Logistics Readiness (weight 0.20)
| Sub-criterion | Max | Source |
|---------------|-----|--------|
| Death certificate path identified | 25 | Jurisdictional vital-records statute |
| Disposition permit / transit permit secured | 25 | State disposition statutes |
| Vendor timeline within `timeline_hours` | 25 | Critical-path planning |
| Contingency for delay (refrigeration/holding) | 25 | Critical-path planning |

### Dimension 4 - Budget Fit (weight 0.20)
Compare itemized plan total vs `budget_usd` using NFDA median benchmarks:
- ratio = plan_total / max(budget_usd, 1).
- ratio <= 0.90 -> 100; <= 1.00 -> 85; <= 1.10 -> 60; <= 1.25 -> 35; > 1.25 -> 15.
- If `budget_usd == 0` (unset), score = 40 and flag for intake follow-up.
- Apply FTC itemized breakdown: basic services + embalming (if consented) + casket/urn +
  outer burial container + facility/use + transportation + cash advances. Each line item
  must come from the GPL; no bundled "package" estimates accepted without itemization.

### Dimension 5 - Consumer Protection (weight 0.15)
| Sub-criterion | Max | Source |
|---------------|-----|--------|
| GPL received and reviewed (FTC 453.2(b)) | 25 | FTC Funeral Rule |
| No mandatory embalming claim (FTC 453.2(c)) | 20 | FTC Funeral Rule |
| Outer-burial-container disclosure (FTC 453.2(d)) | 20 | FTC Funeral Rule |
| Itemized Statement of Goods & Services (FTC 453.2(b)(4)) | 20 | FTC Funeral Rule |
| Cash advances itemized (FTC 453.2(e)) | 15 | FTC Funeral Rule |

## Composite Score
```
composite = 100 * (w1*d1 + w2*d2 + w3*d3 + w4*d4 + w5*d5)
```
where w = {0.20, 0.25, 0.20, 0.20, 0.15} and sum(w) = 1.0.

Weights are surfaced to the user and may be re-weighted per case (e.g., raise
Consumer Protection to 0.25 when an overcharge pattern is detected), but the change MUST be
stated with rationale. Composite is rounded to 1 decimal.

## Evidence Tiers (must be stated per citation)
`Systematic Review > Meta-Analysis > RCT/Empirical > Cohort > Expert Opinion > Knowledge-Base fallback`.
When only the knowledge-base fallback was used, the dimension's confidence is capped at 0.6.

## Outputs
Emit a structured payload (JSON) consumed by `sub-improvement-roadmap`:

```json
{
  "dimensions": {
    "solemnity_appropriateness": { "score": 88.0, "weight": 0.20,
      "subcriteria": [ {"name":"...","points":30,"max":30,"citation":"...","evidence_tier":"..."} ],
      "confidence": 0.9 },
    "rite_completeness":            { "score": 66.7, "weight": 0.25, "...": "..." },
    "logistics_readiness":          { "score": 75.0, "weight": 0.20, "...": "..." },
    "budget_fit":                   { "score": 85.0, "weight": 0.20, "...": "..." },
    "consumer_protection":          { "score": 60.0, "weight": 0.15, "...": "..." }
  },
  "composite": 76.8,
  "weights_used": [0.20, 0.25, 0.20, 0.20, 0.15],
  "weight_rationale": "Default weighting; no overcharge signal detected.",
  "fallback_used": false,
  "assumptions": ["..."],
  "limitations": ["..."]
}
```

## Quality Gate
- [ ] Screener verdict was pass or caution (never block).
- [ ] All 5 dimensions present with sub-criterion points summing to the dimension score.
- [ ] Every sub-criterion carries a `citation` and `evidence_tier`.
- [ ] Weights sum to 1.0 and any non-default weighting is justified.
- [ ] Composite recomputed from dimensions matches the reported `composite` (+/-0.1).
- [ ] Assumptions, confidence, and limitations recorded.
