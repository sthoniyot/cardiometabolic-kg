# Figure captions

## Figure 1. Cardiometabolic knowledge graph at scale.

The full NuGeMi-KG visualised in Neo4j Browser. Nodes are coloured by type
(SNPs, dark blue; genes, orange; phenotypes, red; microbes, cyan; nutrients,
green; foods, yellow); edges by relationship type (Methods §3.2). The graph
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
Biolink Model v3.6 (Methods §3.2.2): for instance, `Snp` *is_a*
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
HNF4A, VEGFA, and ANGPTL4 (Methods §5.2).
