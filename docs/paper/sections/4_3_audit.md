## 4.3 Manual edge audit

To assess data quality beyond automated provenance, we manually audited a
stratified random sample of 25 edges (six to seven per primary edge type)
drawn from the four most novel cross-source edge types: SnpToPhenotype,
FoodToNutrient, MicrobeToNutrient, and MicrobeToGene. The sampling script
uses a fixed random seed (42) and is included in the released code base
(`scripts/select_audit_subset.py`) so that the audit set is reproducible by
third parties.

Each edge was verified against its source reference: PubMed abstracts for
SnpToPhenotype, MicrobeToNutrient, and MicrobeToGene edges; USDA FoodData
Central entries for FoodToNutrient edges. We deliberately applied a strict,
abstract-only verification protocol. An edge was classified VERIFIED only if
the cited source's abstract explicitly stated the encoded relationship between
the source and target entities; PARTIAL if both entities were referenced in
the source and the paper was clearly on-topic, but the abstract did not state
the relationship (typically because it appears only in supplementary tables,
results figures, or full-text passages); UNVERIFIED if the source did not
support the relationship; and NA if the source was inaccessible. This protocol
provides a conservative lower bound on data quality: many published audits use
looser criteria (allowing supplementary-material support), which would shift
PARTIAL edges into VERIFIED.

Of 24 evaluable edges (one SnpToPhenotype source was inaccessible at audit
time and was therefore classified NA), 15 (62%, 95% Wilson CI [43, 79]%) were
classified VERIFIED, 7 (29%, 95% CI [14, 51]%) PARTIAL, and 2 (8%, 95% CI [2,
26]%) UNVERIFIED. Per-edge-type rates are reported in Table 4. The combined
VERIFIED + PARTIAL rate of 91% indicates that essentially all sampled edges
derive from on-topic primary sources; the gap between the strict-VERIFIED
rate (62%) and this combined rate (91%) primarily reflects the limited
information density of abstracts relative to full-text articles, rather than
data quality concerns. The two UNVERIFIED edges, identified during this audit,
are a *Lactiplantibacillus plantarum* → ascorbic acid edge from gutMGene
(*L. plantarum* is a known ascorbate consumer rather than producer in
established biochemistry) and a single SnpToPhenotype edge whose cited cohort
context did not match the indexed disease label. Both have been documented
in our project's issue tracker for upstream curator review and will be
addressed in v1.1 of NuGeMi-KG. Overall, the audit indicates that the KG's
edges are well-grounded in published evidence and that the small number of
problematic edges are individually tractable to identify and correct.
