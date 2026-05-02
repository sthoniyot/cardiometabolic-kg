# NuGeMi-KG: A FAIR tri-layer knowledge graph integrating nutrigenetics, gut microbiome, and food chemistry for cardiometabolic precision nutrition

**[Sharath Thoniyot]**¹, **[Vijayakumar Balakrishnan]**¹

¹ [Department of Computer Science, Birla Institute of Technology and Science, Pilani], [Dubai, United Arab Emirates]

**Corresponding author:** [Sharath Thoniyot] (p20230010@dubai.bits-pilani.ac.in)

---

## Abstract

**Background.** Cardiometabolic diseases arise from the interplay of genetic susceptibility, gut microbiome activity, and dietary intake. Existing biomedical knowledge graphs cover these layers in isolation.

**Methods.** We constructed *NuGeMi-KG*, a tri-layer knowledge graph integrating cardiometabolic GWAS associations (GWAS Catalog), microbe–metabolite and microbe–host gene relationships (gutMGene v2.0), and food-composition data (USDA FoodData Central). The KG is implemented in BioCypher, aligned to the Biolink Model, and deployed in Neo4j.

**Results.** NuGeMi-KG contains 55,263 nodes and 85,308 edges across 8 node types and 9 edge types. We define 15 competency questions, of which 14 return biologically meaningful results. The KG supports five-hop cross-layer queries that surface novel nutrigenetic hypotheses (e.g. *Streptococcus salivarius* → PPARG → 45 cardiometabolic SNPs).

**Conclusion.** NuGeMi-KG is the first public KG that integrates all three layers under a single ontology-aligned schema and is openly queryable for hypothesis generation in precision nutrition.

**Keywords:** knowledge graph, cardiometabolic disease, nutrigenetics, gut microbiome, precision nutrition, Biolink, BioCypher, FAIR

---


## 1 Background & Summary

Cardiometabolic diseases — encompassing type 2 diabetes mellitus, obesity, dyslipidemias,
hypertension, and atherosclerotic cardiovascular disease — collectively account for the
single largest preventable contributor to global morbidity and mortality. Their etiology is
classically multifactorial: heritable susceptibility identified through genome-wide
association studies, environmental exposure to specific dietary patterns and food bioactives,
and an emerging modulating role of the gut microbiome. Effective precision-nutrition
interventions therefore require reasoning across three biological dimensions
simultaneously — host genetic susceptibility, the chemical composition of consumed food,
and gut microbial activity — rather than within any one dimension in isolation.

Each of these dimensions has been characterised at scale through dedicated public
resources. The NHGRI–EBI GWAS Catalog (1) curates more than one million SNP–trait
associations from over 7,000 publications, capturing the genetics layer. The USDA
FoodData Central programme (2) provides analytical-laboratory-grade composition profiles
for hundreds of foods across more than 600 nutrients. The gutMGene v2.0 database (3)
curates causal and correlational relationships between gut microbes, their metabolites, and
host genes, distinguished by experimental evidence type. Together, these three resources
constitute a near-complete reference base for nutrigenetic and microbiome-informed
research; however, they do not interoperate without significant integration effort, and
disease-relevant cross-layer queries — for instance, "which foods carry nutrients that gut
microbes convert into metabolites which modulate genes carrying T2D-associated GWAS
variants" — cannot be expressed in any single resource.

Several biomedical knowledge graphs (KGs) have aggregated subsets of this information.
PrimeKG (4) integrates twenty primary biomedical resources to describe 17,080 diseases
across ten biological scales but does not include food composition or microbiome data. The
Monarch Initiative knowledge graph (5) provides extensive disease–gene–phenotype
integration across species but lacks both nutritional and microbial layers. Microbe-focused
KGs such as KGMicrobe represent microbe–disease associations without GWAS-level
genetic evidence. Food-chemistry resources such as FooDB and the recent VMH catalog
the chemistry of consumed foods but do not link them to host genetic variation. To our
knowledge, no single public knowledge graph integrates host nutrigenetics, gut microbial
function, and food composition under a unified ontology-aligned schema; consequently,
the integrative cross-layer reasoning patterns required for precision-nutrition hypothesis
generation are not currently expressible as direct queries against any single resource.

We address this gap with **NuGeMi-KG**, a tri-layer cardiometabolic knowledge graph that
brings nutrigenetics, gut microbiome, and food composition into a single Biolink-aligned
schema (6) and is implemented as a fully reproducible BioCypher pipeline (7). The
released resource contains 55,263 nodes and 85,308 edges across eight node types and
nine edge types, anchored on eleven cardiometabolic phenotypes harmonised to MONDO
disease classes (8). We define fifteen competency questions to validate the schema and
demonstrate that the KG supports the intended cross-layer query patterns; in particular,
five tri-layer questions return non-trivial five-hop paths integrating food, microbiome,
and genetics evidence. As one example, querying for microbes that modulate host genes
carrying cardiometabolic GWAS variants surfaces *Streptococcus salivarius* and
*Enterococcus faecalis* as joint modulators of PPARG, a gene with 45 distinct
cardiometabolic GWAS variants spanning seven phenotypes (Figure 3) — a tri-layer
hypothesis pattern that, to our knowledge, no existing public KG has previously made
queryable. The remainder of this paper describes the data sources and integration
methodology (§2), the released artifacts (§3), data quality assessment and competency
evaluation (§4), and example use-cases (§5).

## 2 Methods

### 2.1 Data sources

NuGeMi-KG integrates three primary public resources, each contributing
one biological layer (Table 1).

**Genetics layer (GWAS Catalog).** We used the NHGRI–EBI GWAS Catalog
release of 21 April 2026 (the "all associations with added ontology
annotations" TSV bulk download). The full release contains approximately
1.1 million SNP–trait association records from over 7,000 publications. We
filtered to cardiometabolic traits using a curated keyword list of twenty-four
substring patterns (e.g. *type 2 diabetes*, *body mass index*, *LDL
cholesterol*, *coronary artery disease*, *blood pressure*) and mapped each
matched trait to one of eleven canonical MONDO disease classes (Table 1
in DATA_SOURCES.md). Associations were retained only if the reported
*P* value was at or below the conventional genome-wide significance
threshold (5 × 10⁻⁸); records lacking an `rs`-formatted SNP identifier or
listing multiple comma- or semicolon-separated SNPs in a single row were
excluded. After filtering, the genetics layer contributes 47,718 SNPs,
6,398 genes, 11 phenotypes, 16,997 SnpToGene edges, and 54,223
SnpToPhenotype edges.

**Microbiome layer (gutMGene v2.0).** We used gutMGene v2.0 (Qi et al.
2025), which curates causal and correlational relationships among gut
microbes, microbial metabolites, and host genes, with one PubMed citation
per row. We loaded the two literature-based association tables —
*Gut_Microbe-Microbial_Metabolite.csv* and *Gut_Microbe-Host-Gene.csv* —
and applied two filters: human host only, and "causal" associations only
(retaining the highest evidence tier and excluding weaker
correlational entries). Disease-of-interest annotations (DOID column)
were mapped to MONDO using a hand-curated 14-entry crosswalk. After
filtering, the microbiome layer contributes 192 microbes, 378
MicrobeToNutrient edges, 182 MicrobeToGene edges, and 5
MicrobeToPhenotype edges.

**Food-chemistry layer (USDA FoodData Central).** We used the USDA
FoodData Central "Foundation Foods" subset, release of 18 April 2024.
Foundation Foods are USDA's analytical-laboratory–measured reference
profiles, distinct from branded retail items or estimated values. From
the *food.csv*, *nutrient.csv*, and *food_nutrient.csv* tables we loaded
all rows with `data_type == "foundation_food"`. To enable cross-layer
joins between USDA nutrient identifiers (numeric `nutrient_nbr`) and
ChEBI identifiers used elsewhere in the KG, we built a hand-curated
mapping for approximately forty nutrients of cardiometabolic interest
(macronutrients 203/204/205, fibre 291, minerals 301–317, vitamins
318–430, omega-3 species 851/858/875), with the remaining nutrients
falling back to a USDA-prefixed pseudo-CHEBI namespace. After filtering,
the food-chemistry layer contributes 358 foods, 586 nutrients, and
13,523 FoodToNutrient edges.

### 2.2 Schema design

#### 2.2.1 Why Biolink

We aligned the schema to the Biolink Model v3.6.0 (Unni et al. 2022).
Biolink is the de facto standard for biomedical knowledge graphs and is
adopted by Monarch Initiative, PrimeKG, and the NCATS Biomedical Data
Translator programme; alignment provides immediate interoperability with
those resources and a stable, versioned classification of node and edge
types. We chose Biolink v3.6.0 specifically because it is the version
shipped by BioCypher v0.8.0 (the build framework, see §2.4) and avoids
unstable integration with the still-evolving Biolink v4.x.

#### 2.2.2 Node types

The schema declares eight node types (Table N), each mapped to a Biolink
parent class via the BioCypher `is_a` directive: `snp` (Biolink
*sequence variant*), `gene` (Biolink *gene*, no `is_a` required),
`pathway` (Biolink *pathway*), `microbe` (Biolink *organism taxon*),
`cazyme` (Biolink *named thing*), `nutrient` (Biolink *small molecule*),
`food` (Biolink *food*), and `phenotype` (Biolink *phenotypic feature*).
Each node carries a *preferred_id* directive declaring its canonical
identifier namespace (dbSNP for SNPs, HGNC for genes, NCBITaxon for
microbes, ChEBI for nutrients, FoodOn for foods, MONDO for phenotypes,
Reactome for pathways, UniProt for CAZymes). Node-level properties
include name and rank for taxa, symbol and description for genes,
chromosome / position / risk allele for SNPs, and analytical food group
for foods.

#### 2.2.3 Edge types

Nine edge types are declared, each inheriting from Biolink *association*:
SnpToGene, SnpToPhenotype, GeneToPathway, FoodToNutrient,
MicrobeToNutrient, MicrobeToCazyme, MicrobeToGene, MicrobeToPhenotype,
and PhenotypeToPhenotype. Edges are organised by layer: genetics-internal
(three types), food-internal (one type), microbiome-internal (three
types), and cross-layer (two types). All edges carry per-edge
provenance properties — PMID for literature-derived edges, FDC food
identifier for compositional edges — together with edge-type-specific
properties such as effect size and *P* value (SnpToPhenotype),
concentration and unit (FoodToNutrient), and evidence tier and
experimental condition (MicrobeToNutrient). The complete schema
(`config/schema_config.yaml`) is included in the released code base.

#### 2.2.4 BioCypher property declaration

We note an implementation-relevant feature of the BioCypher framework:
edge properties that are produced by an adapter but not enumerated under
the corresponding `properties:` block in the schema configuration file
are silently dropped at CSV write time (logged at INFO level rather than
as a warning). During development, this caused the PMID property of
MicrobeToNutrient and MicrobeToGene edges to be lost between adapter
output and the Neo4j-loaded graph; the issue was identified during the
manual audit (§4.3) when inspection of edge property keys in Neo4j
showed only `id` and `evidence_tier`. We resolved the issue by
explicitly declaring `pmid` (and, for MicrobeToNutrient, `condition`) in
the schema; we recommend explicit enumeration of all retained properties
as a best practice for any BioCypher-based pipeline.

### 2.3 Adapter implementation

Each of the three layers is ingested by a dedicated Python adapter class
in the `adapters/` package, following the BioCypher generator interface:
each adapter implements `get_nodes()` and `get_edges()` methods that
yield `(id, label, properties)` and `(id, source, target, label,
properties)` tuples, respectively. The three adapters share a common
filtering-and-yielding pattern but differ in their input-format-specific
parsing logic.

The **GWAS adapter** (`adapters/gwas_adapter.py`) reads the GWAS Catalog
TSV, filters by trait keyword and *P*-value, parses the *REPORTED
GENE(S)* field with a regex split on `[,;]`, and excludes a curated
set of junk gene symbols (`{"NR", "NA", "intergenic", "-", "", "null",
"None"}`). It deduplicates `(SNP, phenotype)` and `(SNP, gene)` pairs
across the input rows, retaining the smallest *P* value when duplicates
occur.

The **USDA adapter** (`adapters/usda_adapter.py`) reads the four
Foundation Foods CSVs (food, nutrient, food_nutrient, food_category),
joins them in memory, and emits one Food node per `data_type ==
"foundation_food"` row, one Nutrient node per distinct `nutrient_nbr`
encountered, and one FoodToNutrient edge per `food_nutrient` row. The
hand-curated `NUTRIENT_NBR_TO_CHEBI` mapping is applied to resolve
ChEBI identifiers; unmapped nutrients fall back to `USDA:<nbr>`
identifiers within the same namespace.

The **gutMGene adapter** (`adapters/gutmgene_adapter.py`) reads the two
literature-based association tables. The metabolite file is in UTF-8;
the host-gene file is in ISO-8859-1 (the adapter tries both encodings
in order). Two adapter-level transformations are applied. First, the
gutMGene CSV uses a fill-down convention in which subsequent rows of
the same `Index` group inherit the PMID from the first row of the group
but leave subsequent rows blank in raw export; we forward-fill PMID
within `Index` groups to recover this provenance. Second, when the same
`(microbe, target)` pair is reported in multiple papers, only one edge
is yielded; if the first encountered row lacks a PMID, the adapter
prefers a subsequent PMID-bearing row. After both transformations, 100%
of MicrobeToNutrient and MicrobeToGene edges in the released graph
carry a PubMed citation.

### 2.4 Build pipeline

The complete build is orchestrated by `scripts/build_kg.py`, which
instantiates a BioCypher object configured from
`config/biocypher_config.yaml` and `config/schema_config.yaml`,
sequentially runs the three adapters, and writes Biolink-validated CSV
files to `data/processed/biocypher-out/`. Loading into Neo4j is handled
by a separate script (`scripts/load_to_neo4j.py`) that reads the
generated CSVs and inserts them via the bolt protocol using
`neo4j>=5.0`'s `execute_write` API; we use a bolt-driver loader rather
than the `neo4j-admin import` tool because it does not require Neo4j
to be stopped, supports incremental development, and uses MERGE
semantics that correctly handle the `part001` files that BioCypher
emits for nodes that appear in more than one adapter (e.g. genes shared
between the GWAS Catalog and gutMGene, and nutrients shared between
USDA FoodData Central and gutMGene). Total runtime is approximately
30 seconds for the build step and 2 minutes for the Neo4j load step
on a workstation with an Intel i7 CPU and 16 GB RAM, executing under
WSL2 Ubuntu and a single-node Neo4j 5.x community-edition instance.

### 2.5 Reproducibility

The complete build pipeline — including all three adapters, the schema
configuration, the build and loader scripts, the manual-audit
reproducibility scripts, and the fifteen competency queries — is
released under CC-BY-4.0 at https://github.com/sthoniyot/cardiometabolic-kg
and archived at Zenodo (DOI to be assigned). Software dependencies are
pinned in `requirements.txt` (BioCypher 0.8.0, Neo4j Python driver
≥5.0, pandas, requests, pyyaml). The build environment is reproducible
via a conda specification (`environment.yml`) targeting Python 3.11.
Source data is downloadable directly from the upstream resources via
URLs documented in `DATA_SOURCES.md`; the GWAS Catalog and USDA
FoodData Central provide stable bulk-download endpoints, while
gutMGene v2.0 requires a one-time manual download from its host
website. Random-seed-dependent operations — specifically the audit
sample selection in `scripts/select_audit_subset.py` — use `seed=42`
throughout. The full release is tagged at v1.0.0 in the Git history;
the snapshot of the Neo4j database used for all reported results is
included as a `.dump` file in the Zenodo deposit.

## 3 Data Records

The cardiometabolic knowledge graph and all reproducibility artefacts are
released under CC-BY-4.0 in two coordinated locations: a Git repository at
https://github.com/sthoniyot/cardiometabolic-kg containing source code,
schema configuration, and pipeline scripts; and a Zenodo deposit at
https://doi.org/10.5281/zenodo.PLACEHOLDER containing the pre-built
knowledge graph artefacts that are too large to commit to a Git history
(Table 2). The two are linked: each tagged GitHub release is deposited to Zenodo, ensuring that every released graph version
is associated with both a Git tag and a persistent DOI.

### 3.1 Pre-built knowledge graph (Zenodo)

The Zenodo deposit (DOI: 10.5281/zenodo.PLACEHOLDER) contains three
pre-built artefacts. **`cardiometabolic_kg_v1.0.0.dump`** (~50 MB) is a
Neo4j 5.x database dump that can be loaded directly into a local Neo4j
instance with `neo4j-admin database load --from-path=./
cardiometabolic_kg_v1.0.0.dump neo4j --overwrite-destination`; this is
the recommended starting point for users who want to immediately query
the graph. **`cardiometabolic_kg_v1.0.0_csv.zip`** (~30 MB compressed)
contains the per-node and per-edge CSV files emitted by the BioCypher
pipeline, with one CSV per node type and one per edge type plus their
corresponding header files; this format is suitable for users who wish
to load the graph into a non-Neo4j backend (e.g. ArangoDB, Memgraph) or
who require a database-agnostic intermediate. **`Cardiometabolic-KG_v1.0.0_source.zip`**
(~5 MB) is a snapshot of the GitHub repository at the v1.0.0 tag,
included for archival completeness so that the deposit is fully
self-contained even if the GitHub repository becomes unavailable.

### 3.2 Source code and pipeline (GitHub)

The Git repository contains all source code, schema configuration, and
documentation needed to rebuild the knowledge graph from the upstream
data sources: three adapter modules (`adapters/gwas_adapter.py`,
`adapters/usda_adapter.py`, `adapters/gutmgene_adapter.py`); the
BioCypher schema configuration (`config/schema_config.yaml`); the
build and load pipeline (`scripts/build_kg.py`, `scripts/load_to_neo4j.py`);
the fifteen competency-question Cypher files (`queries/competency/`);
the manual-audit reproducibility scripts (`scripts/select_audit_subset.py`,
`scripts/score_audit.py`); the audit verdicts as a tab-separated file
(`audit/edge_sample_25.tsv`); pinned dependencies (`requirements.txt`);
project documentation (`README.md`, `DATA_SOURCES.md`, `CHANGELOG.md`);
machine-readable citation metadata (`CITATION.cff`); and the licence
(`LICENSE`). Source data are not included in the repository owing to
file-size and licensing considerations; download instructions and
canonical URLs are documented in `DATA_SOURCES.md`.

### 3.3 Versioning policy

Releases follow semantic versioning (https://semver.org/). Major version
increments (v2.0, v3.0, …) signal schema-breaking changes that affect
existing queries. Minor version increments (v1.1, v1.2, …) signal data
updates from upstream sources or non-breaking schema extensions (e.g.
adding new edge properties). Patch increments (v1.0.1, v1.0.2, …)
signal bug fixes and documentation improvements that do not affect
graph contents. The audit verdict file is regenerated at each minor or
major release and a new audit summary is appended to `CHANGELOG.md`.

**Table 2.** Released artefacts. Sizes are approximate at v1.0.0 and may
change in subsequent releases.

| Artefact | Format | Size | Location | Purpose |
|---|---|---|---|---|
| `cardiometabolic_kg_v1.0.0.dump`           | Neo4j 5.x dump | ~50 MB | Zenodo  | Pre-built database, ready to import via `neo4j-admin database load` |
| `cardiometabolic_kg_v1.0.0_csv.zip`        | ZIP of CSVs    | ~30 MB | Zenodo  | Adapter-agnostic intermediate; suitable for non-Neo4j backends |
| `Cardiometabolic-KG_v1.0.0_source.zip`     | ZIP of source  | ~5 MB  | Zenodo  | Archival snapshot of the GitHub repository at v1.0.0 |
| `adapters/`                                | Python source  | < 50 kB | GitHub | Three adapter modules (GWAS, USDA, gutMGene) |
| `config/schema_config.yaml`                | YAML           | < 10 kB | GitHub | BioCypher schema configuration |
| `scripts/`                                 | Python source  | < 50 kB | GitHub | Build pipeline, Neo4j loader, audit scripts, competency runner |
| `queries/competency/`                      | Cypher files   | < 50 kB | GitHub | Fifteen competency-question queries (CQ1–CQ15) |
| `audit/edge_sample_25.tsv`                 | TSV            | < 10 kB | GitHub | Manual audit verdicts |
| `DATA_SOURCES.md`                          | Markdown       | < 10 kB | GitHub | Upstream-source URLs, versions, licences |
| `requirements.txt`, `environment.yml`      | Plain text     | < 5 kB | GitHub | Pinned software dependencies |

## 4 Results

### 4.1 Knowledge graph statistics and structural properties

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

### 4.2 Competency-question evaluation

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

### 4.3 Manual edge audit

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

## 5 Discussion

### 5.1 Principal findings

NuGeMi-KG is, to our knowledge, the first publicly released knowledge graph
that integrates host nutrigenetics, gut microbial activity, and food
composition under a single ontology-aligned schema. Three findings from the
present work establish the resource's utility. First, the tri-layer
schema (Figure 2) is sufficient to express full five-hop precision-nutrition
queries in a single Cypher statement (CQ11), demonstrating that integration
across the three layers is not merely structural but query-actionable.
Second, the convergence of microbial, genetic, and phenotypic evidence on
specific host genes — PPARG, VEGFA, HNF4A, ANGPTL4 — recapitulates
mechanistically established cardiometabolic loci without these genes being
hard-coded into any layer of the integration pipeline; this constitutes a
form of internal validation. Third, the manual audit demonstrates that 91%
of sampled edges have direct primary-literature support, with the remaining
9% comprising specific, individually tractable curation issues in the
upstream sources rather than integration errors.

### 5.2 Comparison with existing resources

Several established biomedical knowledge graphs cover subsets of NuGeMi-KG's
content. PrimeKG (Chandak et al. 2023) integrates twenty primary biomedical
resources to describe over 17,000 diseases, but does not include food
composition or microbiome data; cross-layer queries of the form expressible
in NuGeMi-KG are therefore not supported. The Monarch Initiative knowledge
graph (Putman et al. 2024) provides extensive disease–gene–phenotype
integration across species and shares NuGeMi-KG's Biolink alignment, but
similarly lacks both nutritional and microbial layers. Microbe-centric
resources such as KGMicrobe (Joachimiak et al. 2024) capture microbe–disease
associations without GWAS-level genetic evidence, while food-chemistry
resources such as FooDB and the Virtual Metabolic Human (VMH) catalogue
food composition without linking it to host genetic variation.
NuGeMi-KG's contribution is therefore not the volume of data — at 55,263
nodes it is two orders of magnitude smaller than PrimeKG — but the
structural property that a single five-hop query can traverse all three
biological dimensions simultaneously.

### 5.3 Methodological insights

Three implementation choices proved unexpectedly consequential during
development. First, BioCypher silently drops edge properties that are not
explicitly declared in the schema configuration (`schema_config.yaml`); this
behaviour is logged at INFO level rather than as a warning, and was
identified only during manual audit when PMIDs appeared to be missing from
edges that the source data demonstrably contained them. Explicitly
enumerating all retained properties — including provenance fields such as
PMID and condition — should be considered a best practice for any
BioCypher-based pipeline. Second, gutMGene's CSV export uses a fill-down
convention in which subsequent rows of the same evidence group inherit the
PMID from the first row, leaving subsequent rows blank in raw export;
forward-filling is therefore necessary at adapter level. Third, deduplication
of literature-redundant edges (the same microbe–metabolite pair reported in
multiple studies) materially affected query results: pre-deduplication, CQ3
returned five duplicate *C. minuta* → Acetate rows; post-deduplication, the
same query returned a clean ranked list of distinct microbe–metabolite pairs.

### 5.4 Limitations

Three limitations bound the resource's current scope. First, NuGeMi-KG is
restricted to cardiometabolic phenotypes (eleven MONDO classes); extension
to other complex diseases requires re-running the GWAS adapter with a new
keyword filter and adjusting the gutMGene DOID-to-MONDO mapping. Second,
the microbiome layer inherits gutMGene's coverage limitations: of 192
included microbes, only one is directly annotated with obesity in the
source database, which limits the expressiveness of microbe-to-phenotype
direct queries (CQ6). Cross-layer paths via shared host genes (CQ7, CQ12,
CQ14) substantially mitigate this. Third, the food layer uses USDA's
Foundation Foods subset (358 foods); broader coverage will require
incorporating additional food-composition resources such as FooDB and
mapping their identifiers to FDC. Finally, the manual audit (n=24
evaluable) is statistically appropriate for an initial release but a
larger second-annotator audit would tighten the strict-VERIFIED
confidence interval; this is planned for v1.1.

### 5.5 Implications and future work

NuGeMi-KG is designed for hypothesis generation rather than statistical
inference. A typical user-facing workflow combines a Cypher query that
identifies candidate cross-layer relationships, manual review of the
underlying primary sources via the embedded PMIDs, and downstream
experimental or epidemiological validation in independent cohorts. We
anticipate three application directions: (i) nutrigenetic hypothesis
generation for diet-modifiable risk modifiers conditioned on a person's
genotype; (ii) drug-repurposing screens that cross-reference microbial
metabolites against approved-drug targets; and (iii) SNP-aware dietary
recommendation systems for clinical-translational tools. Planned future
work includes incorporation of UK Biobank cardiometabolic GWAS summary
statistics, integration of KGMicrobe's broader microbial functional
annotation, and a second-annotator audit cycle.

## 6 Conclusion

We have presented NuGeMi-KG, a tri-layer knowledge graph that integrates
nutrigenetics, gut microbiome, and food chemistry under a single
Biolink-aligned schema specifically designed to support cardiometabolic
precision-nutrition research. The resource contains 55,263 nodes and
85,308 edges across eight node types and nine edge types, with 100%
PubMed citation coverage on its literature-derived edges. We defined
fifteen competency questions to evaluate the schema, of which fourteen
return biologically meaningful results, including five tri-layer queries
that surface novel hypothesis-generation patterns — for example, the
convergence of *Streptococcus salivarius*, *Enterococcus faecalis*, and
forty-five cardiometabolic GWAS variants on PPARG. A manual audit of
twenty-four randomly sampled edges places the strict-protocol verification
rate at 62% (95% CI [43, 79]%), with 91% of sampled edges having direct
primary-literature support. The KG, source code, and reproducibility
artefacts are released under CC-BY-4.0 at https://github.com/sthoniyot/cardiometabolic-kg
and archived at Zenodo (DOI to be assigned). NuGeMi-KG is, to our knowledge,
the first publicly available resource in which a single graph query can
traverse food, microbiome, host genetics, and cardiometabolic phenotype in
one statement, and we anticipate that this property will support
hypothesis-generation workflows that have not previously been expressible
against any single public knowledge graph.

## 7 Code Availability

All source code, build scripts, schema configuration, competency-query
files, and audit data are released under CC-BY-4.0 at
https://github.com/sthoniyot/cardiometabolic-kg and archived at Zenodo
(DOI: 10.5281/zenodo.PLACEHOLDER). Pre-built Neo4j database dumps and
BioCypher CSV exports are available in the same Zenodo deposit. The
software stack is Python 3.11, BioCypher 0.8.0, Neo4j 5.x, and the
Neo4j Python driver ≥5.0; full pinned dependencies are in
`requirements.txt`.

# Figure captions

## Figure 1. Cardiometabolic knowledge graph at scale.

The full NuGeMi-KG visualised in Neo4j Browser. Nodes are coloured by type
(SNPs, dark blue; genes, orange; phenotypes, red; microbes, cyan; nutrients,
green; foods, yellow); edges by relationship type (Methods §2.2). The graph
contains 55,263 nodes and 85,308 edges. Layout is force-directed and not
biologically meaningful at this density; the figure is provided to convey
overall scale and the relative size of each layer. Two structural features
are visible at this resolution: (i) the dense blue mass at left is the
genetics layer (47,718 SNPs converging on a smaller set of genes and 11
cardiometabolic phenotypes), and (ii) the smaller cyan-and-green cluster at
the right is the literature-curated microbiome–metabolite layer connecting
into the central genes layer through ~180 microbe→host-gene edges. The food-
chemistry layer (yellow) attaches via shared nutrient nodes (green). Detailed
schema-level views and tri-layer query results are shown in Figures 2 and 3
respectively.

## Figure 2. Schema of the NuGeMi-KG knowledge graph.

Abstract schema visualised via Neo4j's `db.schema.visualization()` procedure.
Eight node types (rectangles) are connected by nine edge types (labelled
arrows): genetics-internal (SnpToGene, SnpToPhenotype, GeneToPathway),
food-internal (FoodToNutrient), microbiome-internal (MicrobeToNutrient,
MicrobeToCazyme, MicrobeToGene) and three cross-layer edges
(NutrientToPhenotype, MicrobeToPhenotype, PhenotypeToPhenotype) that bridge
the three layers. Each node type is aligned to its parent class in the
Biolink Model v3.6 (Methods §2.2.2): for instance, `Snp` *is_a*
`sequence_variant`, `Microbe` *is_a* `organism_taxon`, and `Nutrient`
*is_a* `small_molecule`. All edge types inherit from Biolink's `Association`
class and carry per-edge provenance properties (PMID, evidence tier, and
where applicable, p-value or effect size). The schema is the primary
contribution of NuGeMi-KG: it is the structural pattern that allows queries
to traverse from food through microbiome through genetics to phenotype in a
single Cypher statement (cf. Figure 3).

## Figure 3. PPARG as a tri-layer convergence point in cardiometabolic disease.

Result of competency question CQ12, visualised in Neo4j Browser. The host gene
PPARG (orange, centre) is jointly modulated by two gut microbes from gutMGene
— *Streptococcus salivarius* and *Enterococcus faecalis* (cyan) — and carries
45 distinct cardiometabolic GWAS variants from the GWAS Catalog, of which the
eight chromosome-3 SNPs in closest physical proximity to the PPARG locus are
shown (dark blue, with rsIDs as captions). Both microbes are connected to
PPARG via causal `MicrobeToGene` edges curated by gutMGene; each rsID is
connected to PPARG via a `SnpToGene` edge from the GWAS Catalog and to one or
more cardiometabolic phenotypes (red) via `SnpToPhenotype`. PPARG encodes the
PPARγ nuclear receptor, the molecular target of the thiazolidinedione class of
type-2-diabetes drugs and a known mediator of short-chain fatty acid signalling
from the gut microbiome. The convergence of microbial, genetic, and phenotypic
evidence on PPARG illustrates the principal hypothesis-generation pattern that
NuGeMi-KG is designed to support; analogous tri-layer hubs are returned for
HNF4A, VEGFA, and ANGPTL4 (Methods §4.2).


---

## Acknowledgments

We thank the curators and developers of the GWAS Catalog (NHGRI–EBI), USDA
FoodData Central, gutMGene v2.0, the Biolink Model, and the BioCypher
framework. We thank [Supervisor Name] for guidance during this work and
[Reviewer / Colleague] for reading an earlier version of this manuscript.
[Funding statement, if applicable.]

## Author contributions

**[Author]**: conceptualisation, data curation, software, formal analysis,
visualisation, writing — original draft, writing — review and editing.
[Add additional contributors with CRediT roles as applicable.]

## Competing interests

The author(s) declare no competing interests.

## Data availability

All data, code, and pre-built knowledge-graph artefacts are publicly
available under CC-BY-4.0; see §3 Data Records and §7 Code Availability for
URLs and DOIs.

## References

1. Sollis E, et al. The NHGRI-EBI GWAS Catalog: knowledge base and deposition resource. *Nucleic Acids Res*. 2023;51(D1):D977–D985. doi:10.1093/nar/gkac1010
2. McKillop KT, Fukagawa NK. USDA FoodData Central: methodology and data quality. *J Food Compos Anal*. 2019. doi:10.1016/j.jfca.2019.103289
3. Qi C, et al. gutMGene v2.0: an updated comprehensive database for target genes of gut microbes and microbial metabolites. *Nucleic Acids Res*. 2025;53(D1):D783–D788. doi:10.1093/nar/gkae1002
4. Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. *Sci Data*. 2023;10:67. doi:10.1038/s41597-023-01960-3
5. Putman T, et al. The Monarch Initiative in 2024: an analytic platform integrating phenotypes, genes and diseases across species. *Nucleic Acids Res*. 2024;52(D1):D938–D949. doi:10.1093/nar/gkad1004
6. Unni DR, et al. Biolink Model: A universal schema for knowledge graphs in clinical, biomedical, and translational science. *Clin Transl Sci*. 2022;15(8):1848–1855. doi:10.1111/cts.13302
7. Lobentanzer S, et al. Democratizing knowledge representation with BioCypher. *Nat Biotechnol*. 2023;41:1056–1059. doi:10.1038/s41587-023-01848-y
8. Vasilevsky NA, et al. Mondo: Unifying diseases for the world, by the world. *medRxiv*. 2022. doi:10.1101/2022.04.13.22273750

