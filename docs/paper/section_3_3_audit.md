## §3.3 Manual edge audit

To assess data quality beyond automated provenance, we manually audited a
stratified random sample of 25 edges (6–7 per edge type) drawn from the four
primary edge types of the cardiometabolic KG, using a fixed random seed for
reproducibility. Each edge was verified against its source reference: PubMed
abstracts for SnpToPhenotype, MicrobeToNutrient, and MicrobeToGene edges;
USDA FoodData Central entries for FoodToNutrient edges.

We applied a strict abstract-only verification protocol. An edge was classified
VERIFIED only if the cited source's abstract explicitly stated the encoded
relationship between source and target entities; PARTIAL if both entities were
referenced in the source but the abstract did not state the relationship
(typically because it appears in figures, supplementary tables, or full text
only); UNVERIFIED if the source did not support the relationship; and NA if
the source was inaccessible.

Of 24 evaluable edges, 15 (62%, 95% Wilson CI [43, 79]%) were VERIFIED,
7 (29%) PARTIAL, and 2 (8%) UNVERIFIED. Per-edge-type rates are reported in
Table 2. The 91% combined VERIFIED+PARTIAL rate indicates that almost all
edges are derived from on-topic primary sources; the lower strict-VERIFIED
rate primarily reflects the limited information density of abstracts compared
to full-text articles, rather than data quality concerns. The two UNVERIFIED
edges (a *Lactiplantibacillus plantarum* → ascorbic acid edge from gutMGene,
and a SnpToPhenotype edge with mismatched cohort context) have been flagged
for upstream curator review.
