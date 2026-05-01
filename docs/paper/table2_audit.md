# Table 2. Manual edge audit (n=25 sampled, n=24 evaluable, fixed seed=42)

| Edge type | n | Verified | Partial | Unverified | NA | Verified % | 95% Wilson CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| SnpToPhenotype     |  6 |  3 |  2 |  1 |  1 | 50% | [19, 81]% |
| FoodToNutrient     |  6 |  4 |  2 |  0 |  0 | 67% | [30, 90]% |
| MicrobeToNutrient  |  6 |  4 |  1 |  1 |  0 | 67% | [30, 90]% |
| MicrobeToGene      |  6 |  4 |  2 |  0 |  0 | 67% | [30, 90]% |
| **Overall**        | **24** | **15** | **7** | **2** | **1** | **62%** | **[43, 79]%** |

**Verdict definitions:**
- **VERIFIED**: source's abstract explicitly states the encoded relationship.
- **PARTIAL**: source mentions both entities and is on-topic, but the abstract does not state the relationship (typically present in supplementary tables or full-text only).
- **UNVERIFIED**: source does not support the relationship.
- **NA**: source inaccessible.

**Audit reproducibility:** sample selection is in `scripts/select_audit_subset.py` (random seed = 42); audit verdicts are in `audit/edge_sample_25.tsv`; scoring script in `scripts/score_audit.py`.
