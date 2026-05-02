## 3 Methods

### 3.1 Data sources

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

### 3.2 Schema design

#### 3.2.1 Why Biolink

We aligned the schema to the Biolink Model v3.6.0 (Unni et al. 2022).
Biolink is the de facto standard for biomedical knowledge graphs and is
adopted by Monarch Initiative, PrimeKG, and the NCATS Biomedical Data
Translator programme; alignment provides immediate interoperability with
those resources and a stable, versioned classification of node and edge
types. We chose Biolink v3.6.0 specifically because it is the version
shipped by BioCypher v0.8.0 (the build framework, see §3.4) and avoids
unstable integration with the still-evolving Biolink v4.x.

#### 3.2.2 Node types

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

#### 3.2.3 Edge types

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

#### 3.2.4 BioCypher property declaration

We note an implementation-relevant feature of the BioCypher framework:
edge properties that are produced by an adapter but not enumerated under
the corresponding `properties:` block in the schema configuration file
are silently dropped at CSV write time (logged at INFO level rather than
as a warning). During development, this caused the PMID property of
MicrobeToNutrient and MicrobeToGene edges to be lost between adapter
output and the Neo4j-loaded graph; the issue was identified during the
manual audit (§5.3) when inspection of edge property keys in Neo4j
showed only `id` and `evidence_tier`. We resolved the issue by
explicitly declaring `pmid` (and, for MicrobeToNutrient, `condition`) in
the schema; we recommend explicit enumeration of all retained properties
as a best practice for any BioCypher-based pipeline.

### 3.3 Adapter implementation

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

### 3.4 Build pipeline

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

### 3.5 Reproducibility

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
