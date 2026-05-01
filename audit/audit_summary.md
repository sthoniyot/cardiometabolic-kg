# Audit summary

_Audited: 25 of 25 sampled edges_

## Per-edge-type results

| Edge type | n | Verified | Partial | Unverified | NA | Verified % | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| FoodToNutrient | 6 | 4 | 2 | 0 | 0 | 67% | 30–90% |
| MicrobeToGene | 6 | 4 | 2 | 0 | 0 | 67% | 30–90% |
| MicrobeToNutrient | 6 | 4 | 1 | 1 | 0 | 67% | 30–90% |
| SnpToPhenotype | 6 | 3 | 2 | 1 | 1 | 50% | 19–81% |
| **OVERALL** | **24** | **15** | **7** | **2** | **1** | **62%** | **43–79%** |

## Draft paragraph for §3.3

To assess data quality beyond automated provenance, we manually audited a stratified random sample of 25 edges (≈6 per edge type) drawn from the four primary edge types of the cardiometabolic KG. Each edge was verified against its source reference: PubMed abstracts for SnpToPhenotype, MicrobeToNutrient, and MicrobeToGene edges; USDA FoodData Central entries for FoodToNutrient edges. An edge was classified as VERIFIED if the source explicitly stated the encoded relationship between source and target entities; PARTIAL if both entities were referenced in the source but the relationship was not stated in the abstract (typically described in supplementary figures or full-text tables); UNVERIFIED if the source did not support the relationship; and NA if the source was inaccessible. Of 24 evaluable edges, 15 (62%, 95% CI [43, 79]%) were classified VERIFIED, 7 (29%) PARTIAL, and 2 (8%) UNVERIFIED. Per-edge-type rates are reported in Table 2.