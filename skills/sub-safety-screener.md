---
name: funeral-memorial-planning-sub-safety-screener
description: HARD GATE. Detect acute grief crisis / suicidal ideation / self-harm / vulnerable-person risk and surface bereavement support before any funeral logistics are discussed.
---

## Role
Sub-skill of `funeral-memorial-planning` (Funeral / Memorial Planning Support (custom & religion)).
Acts as the **safety / risk / compliance HARD GATE**. It runs immediately after intake and
**MUST pass before any scores, plans, vendor logistics, or roadmap items are produced.**

## Frameworks Applied
- Kuebler-Ross grief stage model (Kuebler-Ross, 1969, *On Death and Dying*).
- Stroebe & Schut Dual Process Model of coping with bereavement (Death Studies, 1999, 23(3):197-224).
- American Foundation for Suicide Prevention (AFSP) & SAMHSA crisis-line guidance.
- FTC Funeral Rule (16 CFR Part 453) - only the *consumer-protection* axis is screened here
  for coercion/overcharge vulnerability; pricing compliance is scored downstream.

## Inputs
- `intake_payload`: structured object from `sub-profile-intake` containing at minimum
  `free_text`, `emotional_state` (free text or one of
  `stable | grieving | acute | crisis | unknown`), `tradition`, `relationship`, `budget`, `timeline`.
- Optional `prior_messages` (string) for context.

## Blocking Conditions (HARD STOP if ANY is true)
A signal is tripped if any of the high-risk patterns below are present in `free_text` or
`emotional_state`. Detection is conservative - when in doubt, trip.

### A. Acute crisis / suicidal ideation
Patterns (case-insensitive, word-boundary aware) that trip the gate:
- self-harm intent: "kill myself", "end it all", "don't want to live", "suicide",
  "take my own life", "better off dead", "no reason to live", "hurt myself".
- active hopelessness with plan/means: phrases pairing "hopeless"/"can't go on"/"giving up"
  with "pills"/"gun"/"rope"/"noose"/"bridge"/"jump"/"overdose".
- explicit emotional state value `crisis`.

### B. Vulnerable-person / coercion risk
- User states they are a minor, under guardianship, or being pressured/coerced by a funeral
  home or family member ("they won't let me see the price list", "forced to sign",
  "won't give me the GPL").
- Signs of incapacity: intoxication, severe dissociation, or inability to recall the deceased
  ("who died" / "not sure who this is for").

### C. Acute traumatic loss
- Death occurred within the last 0-72 hours AND `emotional_state` is `acute` or `crisis`.
- Death by homicide, suicide of the deceased, or mass-casualty event.

## Procedure
1. Normalize text: lowercase, strip extra whitespace, run pattern match against lists A/B/C.
2. Compute `risk_level` in {`clear`, `caution`, `block`}.
   - `clear`: no pattern matched, `emotional_state` not in {crisis, acute-with-recent-loss}.
   - `caution`: low-grade hopelessness language present but no plan/means; recent loss (<=72h)
     with `grieving` state. Allow planning but emit bereavement resources and soft-pause once.
   - `block`: any A or B pattern matched, or C criteria met.
3. If `risk_level == block`:
   a. STOP the harness. Do not call the scoring engine or roadmap builder.
   b. Emit the referral block (see Outputs).
   c. Offer to continue only with non-logistics, non-financial emotional support framing.
4. If `risk_level == caution`:
   a. Continue but prepend bereavement resources to the final artifact.
   b. Down-weight any cost/discount messaging tone; keep solemnity high.
5. If `risk_level == clear`: proceed normally; still attach a single bereavement-resource
   footer (grief is presumed present in this domain).
6. Record assumptions, the matched patterns (if any), and confidence.

## Outputs
Emit a structured payload (JSON) consumed by the scoring engine:

```json
{
  "verdict": "pass | caution | block",
  "risk_level": "clear | caution | block",
  "matched_patterns": ["A.suicidal_ideation", "C.recent_loss"],
  "referral_issued": true,
  "resources": ["..."],
  "assumptions": ["..."],
  "confidence": 0.0
}
```

When `verdict == block`, also emit the human-facing referral block:

> **You don't have to go through this alone.** If you are thinking about suicide, harming
> yourself, or feel unsafe, please reach out right now:
> - **988 Suicide & Crisis Lifeline** (US): call or text **988**, available 24/7.
> - **SAMHSA National Helpline** (US): 1-800-662-4357 (HELP), 24/7, free and confidential.
> - **Crisis Text Line**: text **HOME** to **741741**.
> - **Veterans Crisis Line**: dial 988 then press 1.
> - **International Association for Suicide Prevention (IASP)** crisis centres:
>   https://www.iasp.info/resources/Crisis_Centres/
>
> When you are ready, I will help you plan with care. There is no rush.

For **caution**, attach the same block in a softer tone plus:
> SAMHSA Disaster Distress Helpline: 1-800-985-5990 | grief-specific support:
> TAPS (survivors of loss) https://www.taps.org/ | Dougy Center (grieving children)
> https://www.dougy.org/

## Quality Gate (must be true before payload is released downstream)
- [ ] All three pattern classes (A/B/C) explicitly evaluated and recorded.
- [ ] `verdict` is one of {pass, caution, block} and matches `risk_level`.
- [ ] If `block`, no scoring/roadmap payload was generated by this stage.
- [ ] Referral resources present and use the verified numbers/links above (not invented).
- [ ] Confidence and matched-pattern rationale recorded.
