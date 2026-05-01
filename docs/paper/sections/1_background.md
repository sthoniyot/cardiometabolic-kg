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
