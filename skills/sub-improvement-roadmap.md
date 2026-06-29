---
name: funeral-memorial-planning-sub-improvement-roadmap
description: Produce a prioritized, culturally-correct improvement roadmap with FTC-transparent cost itemization, effort x impact ranking, and devil's-advocate-ready actions. Stage 5 of the harness.
---

## Role
Sub-skill of `funeral-memorial-planning` (Funeral / Memorial Planning Support (custom & religion)).
Consumes the scoring payload and produces a prioritized, respectful, FTC-transparent roadmap
that the main harness then submits to the devil's-advocate quality gate.

## Frameworks Applied
- FTC Funeral Rule (16 CFR Part 453) - every cost action must be itemized from the GPL.
- Major-tradition rites canon - rite sequencing must be culturally correct.
- Event-logistics critical-path planning - timeline sequencing with slack and contingency.
- NFDA median cost benchmarks - budget anchor for "expected cost" guidance.
- Stroebe & Schut Dual Process Model - tone and pacing respect grief stage.

## Inputs
- `scoring_payload` from `sub-scoring-engine` (all 5 dimensions + composite + sub-criteria).
- `intake_payload` (for tradition, budget, timeline, disposition).

## Procedure
1. For each dimension scoring < 80, generate one or more improvement actions targeting
   the weakest sub-criteria (lowest points-to-max ratio first).
2. Every action MUST include: `action`, `effort` (S/M/L), `impact` (S/M/L), `owner`,
   `expected_effect` (which sub-criterion it raises and by how many points),
   `cost_usd_range` (low-high), `citation`, and `timeline_window`.
3. Sort actions by `priority_score = impact_weight * impact - effort_weight * effort`,
   where impact_weight=1.0, effort_weight=0.5, and L/M/S map to 3/2/1.
4. Sequence rite actions in culturally-correct order (see tradition sequencing below).
5. Itemize every cost from the GPL; never present a bundled "package" price without breakdown.
6. Add a contingency line for delays (refrigeration/holding, alternate venue).
7. Flag any action that needs intake follow-up (e.g., GPL not in hand -> first action).

## Tradition Rite Sequencing (must be honored in the roadmap order)
- **Catholic**: Vigil/Wake (eve) -> Funeral Mass/Liturgy (day) -> Rite of Committal (cemetery).
- **Muslim**: Ghusl (washing) -> Kafan (shrouding) -> Janazah prayer -> Dafan (burial, <=24h).
- **Jewish**: Shmira (watching) -> Taharah (purification) -> Tachrichim (shroud) ->
  Levayah (procession) -> Kevurah (burial) -> Shiva (7 days) -> Shloshim (30 days).
- **Hindu**: Preparation at home -> cremation (<=24h) -> Asthi Visarjan (ash immersion) ->
  13-day Sutak mourning -> Shraddha.
- **Buddhist**: chanting at time of death -> wake/merit transfer -> funeral service ->
  7th-day observance -> 49th-day observance.
- **Secular**: gathering/visitation -> eulogy/celebration of life -> committal/symbolic act.

## FTC Itemized Cost Template (every roadmap must expose this)
```
Basic services of funeral director & staff ........ $____
Emalming (only if consented; not required by law) ... $____  [opt-out available]
Other preparation of the body ...................... $____
Viewing/visitation facility use ..................... $____
Funeral ceremony facility use ........................ $____
Transfer of remains to funeral home .................. $____
Hearse/local transportation ......................... $____
Casket / urn (third-party allowed) .................. $____  [external casket accepted]
Outer burial container (disclose state-cemetery rule). $____  [grade options given]
Cash advances (flowers, obituary, police escort)... $____  [itemized, passed at cost]
                                                    --------
Subtotal before disposition ....................... $____
Disposition (crematory/cemetery/sea) ............... $____
                                                    --------
TOTAL .............................................. $____
```
Every blank is filled from the GPL the user obtained. If `gpl_in_hand == false`, the FIRST
roadmap action is "Request the General Price List in writing (FTC right)."

## Outputs
Emit a structured payload (JSON) for the devil's-advocate quality gate:

```json
{
  "roadmap": [
    {
      "id": 1,
      "action": "Request written General Price List from the funeral home.",
      "effort": "S", "impact": "L", "owner": "family",
      "expected_effect": "consumer_protection.GPL +25",
      "cost_usd_range": [0, 0],
      "citation": "FTC Funeral Rule 16 CFR 453.2(b)",
      "timeline_window": "0-24h",
      "priority_score": 2.5
    }
  ],
  "rite_sequence": ["vigil", "funeral_mass", "rite_of_committal"],
  "cost_itemization": { "basic_services": 2100, "embalming": 0, "casket": 1495, "...": "..." },
  "total_estimate_usd": 5895,
  "budget_usd": 6000,
  "budget_variance_usd": -105,
  "contingency": "Refrigerated holding 24h at $75/day if burial delayed.",
  "assumptions": ["..."],
  "limitations": ["..."]
}
```

## Quality Gate
- [ ] Every dimension < 80 produced at least one targeted action.
- [ ] Every action has effort + impact + owner + expected_effect + cost range + citation.
- [ ] Rite actions are in culturally-correct sequence for the declared tradition.
- [ ] Cost itemization is a complete FTC breakdown (no bundled "package" prices).
- [ ] If GPL was not in hand, action #1 is the GPL request.
- [ ] Contingency line present.
- [ ] Assumptions and limitations recorded.
