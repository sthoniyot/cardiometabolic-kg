**Table 4.** Manual audit of 25 stratified-random edges (24 evaluable; one SnpToPhenotype source was inaccessible at audit time). Verification rates use Wilson 95% confidence intervals.

| Edge type | n | Verified | Partial | Unverified | NA | Verified % | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| SnpToPhenotype     |  6 |  3 |  2 |  1 |  1 | 50% | [19, 81]% |
| FoodToNutrient     |  6 |  4 |  2 |  0 |  0 | 67% | [30, 90]% |
| MicrobeToNutrient  |  6 |  4 |  1 |  1 |  0 | 67% | [30, 90]% |
| MicrobeToGene      |  6 |  4 |  2 |  0 |  0 | 67% | [30, 90]% |
| **Overall**        | **24** | **15** | **7** | **2** | **1** | **62%** | **[43, 79]%** |

**Verdict definitions.** VERIFIED: source's abstract explicitly states the encoded relationship. PARTIAL: source mentions both entities and is on-topic, but the abstract does not state the relationship (typically present in supplementary tables, results figures, or full text only). UNVERIFIED: source does not support the relationship. NA: source inaccessible at audit time.

**Reproducibility.** Sampling: `scripts/select_audit_subset.py`, seed=42; verdicts: `audit/edge_sample_25.tsv`; scoring: `scripts/score_audit.py`.
