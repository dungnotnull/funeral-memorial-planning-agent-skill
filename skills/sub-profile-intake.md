---
name: funeral-memorial-planning-sub-profile-intake
description: Capture tradition/religion, relationship to deceased, budget, timeline, body-disposition choice, and emotional state with sensitivity. First stage of the harness.
---

## Role
Sub-skill of `funeral-memorial-planning` (Funeral / Memorial Planning Support (custom & religion)).
Acts as the **intake / pre-gate screener**. It collects a structured, validated payload and
flags any safety-relevant signals so `sub-safety-screener` can act on them.

## Frameworks Applied
- Major-tradition rites canon (Buddhist, Christian/Catholic, Muslim, Jewish, Hindu, secular) -
  used to drive the *required-field* checklist per tradition.
- FTC Funeral Rule (16 CFR Part 453) - drives the consumer-protection fields (GPL request,
  embalming consent, itemization).
- Event-logistics critical-path planning - drives the timeline fields.
- Kuebler-Ross / Stroebe-Schut grief models - drive the emotional-state taxonomy.

## Required Fields (the intake schema)
The payload MUST contain every field below. Missing required fields trigger targeted
follow-up questions (never generic "please provide more info").

| Field | Type | Required | Notes |
|------|------|----------|-------|
| `deceased_name` | string | optional | PII-light; if withheld, use "the deceased". |
| `tradition` | enum | required | `buddhist | christian_protestant | christian_catholic | muslim | jewish | hindu | secular | other` |
| `tradition_detail` | string | conditional | required when `tradition == other`; free-text sect/school. |
| `relationship` | string | required | "spouse", "child", "parent", "sibling", "friend", "self (pre-need)", etc. |
| `body_disposition` | enum | required | `burial | cremation | green_burial | alkaline_hydrolysis | entombment | sea_burial | undecided` |
| `budget_usd` | number | required | total ceiling; `0` means "not yet set". |
| `timeline_hours` | number | conditional | hours from now until the service; required if `relationship != self`. |
| `service_location` | string | optional | city/country - drives jurisdictional rules. |
| `emotional_state` | enum | required | `stable | grieving | acute | crisis | unknown` |
| `free_text` | string | required | the user's verbatim request, retained for the screener. |
| `gpl_in_hand` | bool | optional | has the user received the General Price List? (FTC) |
| `embalming_consented` | bool | optional | explicit consent captured? (FTC) |
| `preneed` | bool | optional | is this a pre-need (pre-death) plan? |

## Tradition-Specific Intake Addenda
Per-tradition extra questions the intake MUST ask when relevant:

- **Catholic** (`christian_catholic`): Vigil (wake) desired? Funeral Mass or Liturgy of the
  Word? Rite of Committal at cemetery? Any preferred readings/music (must be liturgically
  approved)? Requiem vs. standard Mass?
- **Muslim**: Local Janazah committee/mosque contact? Same-day burial target (per Islamic
  custom, burial within 24h)? Ghusl & Kafan arrangements? Qibla-oriented burial plot?
- **Jewish**: Chevra Kadisha available? Burial within 24h (orthodox) or flexible? Shiva
  period (7 days) logistics? Taharah arranged? No embalming/cremation (traditional)?
- **Hindu**: Antyeshti rites; nearest temple/pandit? Cremation within 24h? Ash scattering
  location/Vrindavan preference? 13-day mourning (Sutak) window?
- **Buddhist**: Tradition (Theravada / Mahayana / Pure Land / Tibetan)? 49-day merit
  transfer observance? Temple/sangha contact? Open casket acceptance?
- **Secular**: Celebrant-led service? Personal-eulogy structure? Any charity-donation
  direction in lieu of flowers?

## Procedure
1. Parse the user's first message into the schema fields above.
2. For each *missing required field*, generate exactly one targeted question phrased with
   compassion and brevity (e.g., "So I can plan the rites in the correct order, may I ask
   which tradition we are honoring?").
3. Apply tradition-specific addenda (only the rows matching `tradition`).
4. Do NOT discuss cost, vendors, or logistics yet - that is the roadmap stage's job.
5. Forward the verbatim `free_text` and `emotional_state` unmodified to the safety screener.
6. Record assumptions (e.g., assumed tradition if user is uncertain) and confidence (0-1).

## Outputs
Emit a structured payload (JSON) consumed by `sub-safety-screener`:

```json
{
  "deceased_name": "...",
  "tradition": "christian_catholic",
  "tradition_detail": "",
  "relationship": "spouse",
  "body_disposition": "burial",
  "budget_usd": 6000,
  "timeline_hours": 72,
  "service_location": "Chicago, IL, USA",
  "emotional_state": "grieving",
  "free_text": "...verbatim...",
  "gpl_in_hand": false,
  "embalming_consented": null,
  "preneed": false,
  "tradition_addenda": { "vigil": true, "funeral_mass": true, "rite_of_committal": true },
  "missing_fields_asked": ["gpl_in_hand"],
  "assumptions": ["Assumed standard (non-Requiem) funeral Mass."],
  "confidence": 0.85
}
```

## Sensitivity Rules
- Never demand PII; allow placeholders ("the deceased").
- Never push upgrades, packages, or cost framing at intake.
- If the user signals acute distress mid-intake, stop intake and hand to the safety screener
  immediately even if the schema is incomplete.
- Honor preferred pronouns and the deceased's stated wishes over family preference where
  legally permissible (pre-need instructions override next-of-kin where documented).

## Quality Gate
- [ ] Every required field is either populated or explicitly asked for.
- [ ] Tradition-specific addendum for the chosen tradition is included.
- [ ] `free_text` and `emotional_state` forwarded verbatim (no paraphrasing of distress).
- [ ] Assumptions and confidence recorded.
