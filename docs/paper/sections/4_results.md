## 5 Results

### 5.1 Knowledge graph statistics and structural properties

The released NuGeMi-KG contains 55,263 nodes distributed across eight node
types and 85,308 edges distributed across nine edge types (Table 2). The
genetics layer contributes the largest share of nodes (47,718 SNPs, 6,398
genes, 11 phenotypes), reflecting the GWAS Catalog's broad cardiometabolic
coverage. The microbiome layer is more selective by design — gutMGene's
strict human-only, causal-only filter retains 192 microbes, 378 microbe →
metabolite edges, and 182 microbe → host gene edges, all with PubMed
citations. The food-chemistry layer comprises 358 USDA Foundation Foods
linked to 586 nutrients via 13,523 composition edges. Cross-source
overlap — i.e. nutrient nodes shared between USDA and gutMGene, or gene
nodes shared between GWAS Catalog and gutMGene — is non-trivial and
explicitly preserved by the build pipeline (76 shared genes, 126 shared
nutrient nodes), enabling the cross-layer queries described in §4.3.

Provenance coverage is complete on all literature-derived edge types: 100%
of the 54,223 SnpToPhenotype edges, 100% of the 378 MicrobeToNutrient
edges, and 100% of the 182 MicrobeToGene edges carry a PubMed identifier.
FoodToNutrient edges, drawn from USDA's analytical-laboratory programme,
are accompanied by source-specific provenance (FDC food identifiers and
analytical method codes) rather than per-edge PMIDs.

### 5.2 Competency-question evaluation

We defined fifteen competency questions (CQ1–CQ15) to evaluate whether the
KG supports the intended biomedical query patterns (Table 3). The questions
are organised by layer depth: five Tier-1 (single-layer) queries probe
within-layer correctness; five Tier-2 (two-layer) queries probe pairwise
cross-layer integration; and five Tier-3 (tri-layer) queries probe the
full Food → Microbiome → Genetics → Phenotype chain that constitutes the
resource's principal contribution.

Of the fifteen questions, fourteen return non-empty, biologically meaningful
results. Tier-1 queries recover canonical findings: CQ1 returns the
TCF7L2 rs7903146 variant with an odds ratio of 1.36 for type 2 diabetes
mellitus, matching published meta-analyses; CQ2 returns coconut flour, ground
flaxseed, and rye flour as the highest-fibre Foundation Foods (34.2, 23.1,
13.7 g/100g respectively); CQ3 returns *Christensenella minuta*,
*[Clostridium] scindens*, and *various Eubacterium species* among the top butyrate
producers. CQ4 returns ADAMTSL3, LPL, and FAM101A as the most cardiometabolic-
GWAS-rich genes (75, 71, and 67 distinct SNPs respectively), recovering LPL —
lipoprotein lipase, a textbook lipid-metabolism gene — at rank 2.

Tier-2 queries demonstrate the schema's cross-layer reasoning capacity. CQ7,
which retrieves microbes whose modulated host genes also carry cardiometabolic
GWAS variants, returns fifteen microbe–gene pairs spanning seven cardiometabolic
phenotypes; *Streptococcus salivarius* and *Enterococcus faecalis* jointly
implicate PPARG with 45 distinct GWAS variants, while *Lactiplantibacillus
plantarum* implicates VEGFA with 16 SNPs and HNF4A with 9 SNPs. CQ10 confirms
that rs7903146 is associated with seven distinct cardiometabolic phenotypes
in the KG (T2D, hyperglycemia, obesity, hypercholesterolemia, hypertriglyceridemia,
hypertension, and coronary artery disease), recovering the textbook pleiotropy
of this variant.

The five Tier-3 queries are the resource's intended novel contributions. CQ11
returns ten complete five-hop paths of the form Food → Nutrient ← Microbe →
Gene ← SNP → Phenotype; for example, *Strawberries → Vitamin C ← L. plantarum
→ ITCH ← rs117075207 → obesity*. CQ12 surfaces PPARG as a tri-layer
convergence point with two microbial modulators and 45 cardiometabolic SNPs
spanning seven phenotypes (Figure 3). CQ13 generalises this to a ranked list
of bridge genes supported by both microbial modulation and GWAS evidence
(PPARG, VEGFA, HNF4A, ANGPTL4 lead the list, all established metabolic loci).
CQ14 retrieves SCFA-producing microbes that reach obesity or T2D via host-
gene modulation: *Streptococcus salivarius* (butyrate) → PPARG → obesity (39 of the 45 PPARG SNPs are obesity-associated); *Bifidobacterium longum* (acetate) → CYP7A1 → obesity (3 SNPs);
*Akkermansia muciniphila* (acetate) → TNF → obesity. CQ15 produces an
evidence-density map showing densest tri-layer coverage for obesity (24
microbes, 18 genes, 21,521 SNPs), followed by hypertriglyceridemia and
hypercholesterolemia.

The single empty query (CQ6) reflects sparse direct annotation of obesity-
microbe edges in gutMGene v2.0 (only one microbe — *Faecalibacterium
prausnitzii* — has a direct MicrobeToPhenotype association in the source
database), rather than an integration failure; we discuss this limitation in
§5. Mean Cypher latency across the fifteen queries was 5 ms on a single-node
Neo4j 5.x instance running on commodity hardware (Intel i7, 16 GB RAM),
indicating the KG is interactively queryable at this scale.

### 5.3 Manual edge audit

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
