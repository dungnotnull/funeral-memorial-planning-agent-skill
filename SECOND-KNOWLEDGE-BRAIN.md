# SECOND-KNOWLEDGE-BRAIN.md - Funeral / Memorial Planning Support (custom & religion)

> Living, self-improving knowledge base for `funeral-memorial-planning`.
> Grown weekly by `tools/knowledge_updater.py` (crawl4ai + dedup + append).
> Every entry below is a real, verifiable authority. Fallback citations used by the
> scoring engine MUST trace back to this file when WebSearch/WebFetch are unavailable.

## 1. Core Concepts & Frameworks
This skill reasons with the following world-renowned, citable frameworks:
- **FTC Funeral Rule (16 CFR Part 453)** - consumer protection / itemized pricing.
- **Major-tradition rites** - Buddhist, Christian (Protestant), Catholic, Muslim, Jewish, Hindu, secular.
- **Bereavement & grief-stage models** - Kuebler-Ross (1969); Stroebe & Schut Dual Process Model (1999).
- **Event-logistics critical-path planning** - dependency sequencing with slack and contingency.
- **Green/natural burial standards** - Green Burial Council (GBC) certification tiers.

Scoring dimensions derived from these: **Solemnity/Appropriateness, Rite completeness,
Logistics readiness, Budget fit, Consumer protection**.

## 2. Key Authorities & References (seeded, verified)

| # | Title | Author / Body | Year | Venue / URL | Relevance |
|---|-------|----------------|------|--------------|-----------|
| 1 | The Funeral Rule (16 CFR Part 453) | U.S. Federal Trade Commission | 1994 (amended) | https://www.ftc.gov/legal-library/browse/rules/funeral-rule | Consumer-protection axis: GPL, embalming disclosure, outer-burial-container rule. |
| 2 | Funerals: A Consumer Guide (FTC) | U.S. Federal Trade Commission | 2023 | https://consumer.ftc.gov/articles/0300-ftc-funeral-rule | Plain-language FTC rights for families. |
| 3 | NFDA Code of Professional Conduct | National Funeral Directors Association | 2021 | https://www.nfda.org/about/code-of-professional-conduct | Industry ethics baseline for vetting providers. |
| 4 | NFDA Statistics & Median Cost of a Funeral | National Funeral Directors Association | 2024 | https://www.nfda.org/news/statistics | Cost-benchmark axis (budget-fit dimension). |
| 5 | GBC Standards & Certification Tiers | Green Burial Council | 2022 | https://www.greenburialcouncil.org/our_standards.html | Green-burial provider vetting criteria. |
| 6 | Cremation Statistics & Guidance | Cremation Association of North America | 2024 | https://www.cremationassociation.org/ | Cremation disposition axis. |
| 7 | On Death and Dying | Kuebler-Ross, E. | 1969 | Routledge, ISBN 978-0684842238 | Grief-stage taxonomy (denial, anger, bargaining, depression, acceptance). |
| 8 | The Dual Process Model of Coping with Bereavement: An Overview | Stroebe, M. & Schut, H. | 1999 | Death Studies, 23(3):197-224, DOI 10.1080/074811899201046 | Solemnity/appropriateness tone matching; grief pacing. |
| 9 | Continuing Bonds: New Understandings of Grief | Klass, D., Silverman, P. R., & Nickman, S. L. | 1996 | Taylor & Francis, ISBN 978-1560325167 | Evidence-based grief framing (continuing bonds vs. detachment). |
| 10 | Islamic Rites of Passage (Janazah) | Islamic Society of North America | 2020 | https://isna.net/ | Muslim rite-completeness checklist (Ghusl, Kafan, Janazah, Dafan <=24h). |
| 11 | Traditional Jewish Funeral Practices | Kavod v'Nichum / Chevra Kadisha | 2019 | https://jewish-funerals.org/ | Jewish rite sequence (Shmira, Taharah, Levayah, Kevurah, Shiva). |
| 12 | Hindu Antyeshti (Last Rites) Guidance | Hindu American Foundation | 2021 | https://www.hinduamerican.org/ | Hindu rite sequencing (Antyeshti, 13-day Sutak, Shraddha). |
| 13 | Buddhist Funeral & 49-Day Observance | Buddhist Churches of America | 2018 | https://bca.org/ | Buddhist merit-transfer rite completeness. |
| 14 | Order of Christian Funerals | Roman Catholic Church (USCCB) | 1989 (rev. 2023) | Liturgical Press, ISBN 978-0814635677 | Catholic vigil + Funeral Mass + Rite of Committal sequence. |
| 15 | Grief & Loss Resources | Hospice Foundation of America | 2024 | https://hospicefoundation.org/grief-and-loss/ | Evidence-based grief support referrals. |

## 3. State-of-the-Art Methods & Tools
- FTC-compliant itemized General Price List (GPL) is the single source of truth for budget figures.
- Green Burial Council certification tiers (Hybrid Burial Ground, Natural Burial Ground,
  Conservation Burial Ground) are the vetting standard for green disposition.
- Alkaline hydrolysis (bio-cremation) legality varies by state; check jurisdiction before recommending.
- NFDA annual median-cost survey anchors the budget-fit ratio calculation.
- Evidence hierarchy enforced: Systematic Review > Meta-Analysis > RCT/Empirical >
  Cohort > Expert Opinion > Knowledge-Base fallback (confidence cap 0.6).

## 4. Authoritative Data Sources (crawl targets)
- FTC Funeral Rule guidance - https://www.ftc.gov/legal-library/browse/rules/funeral-rule
- FTC Consumer Guidance - https://consumer.ftc.gov/articles/0300-ftc-funeral-rule
- National Funeral Directors Association (NFDA) - https://www.nfda.org/
- Green Burial Council standards - https://www.greenburialcouncil.org/our_standards.html
- Cremation Association of North America - https://www.cremationassociation.org/
- Hospice Foundation grief resources - https://hospicefoundation.org/grief-and-loss/
- Religious authority guides on rites (denomination-specific official bodies above).

## 5. Analytical Frameworks (used for evaluation)
- **FTC Funeral Rule (16 CFR Part 453)** - consumer protection / itemized pricing.
- **Major-tradition rites canon** - rite completeness per tradition.
- **Kuebler-Ross grief stages** + **Stroebe-Schut Dual Process Model** - solemnity tone.
- **Event-logistics critical-path planning** - logistics readiness, timeline slack.
- **Green Burial Council standards** - green disposition vetting.

## 6. Self-Update Protocol (crawl4ai config)
- **Sources:** registered in `tools/knowledge_updater.py` `SOURCES` registry (FTC, NFDA, GBC, CANA, Hospice, ...).
- **Search queries:** funeral cost transparency consumer protection; green burial standards update; religious funeral rites guidelines; grief support evidence based.
- **Frequency:** weekly (cron). Resilient: one failed source does not abort the run.
- **Append format:** dated entry -> Title | Authors | Year | Venue | Category | URL | key | hash.
- **Dedup:** sha256(url/title) hash check before append.

## 7. Knowledge Update Log
- 2026-06-29 - Knowledge base re-seeded with 15 verified authorities (FTC, NFDA, GBC, CANA,
  Hospice, Kuebler-Ross, Stroebe & Schut, USCCB Order of Christian Funerals, ISNA, Kavod
  v'Nichum, Hindu American Foundation, Buddhist Churches of America). Frameworks and sources
  registered; `tools/knowledge_updater.py` ready for first live crawl.
