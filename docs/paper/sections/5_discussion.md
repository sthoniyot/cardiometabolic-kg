## 6 Discussion

### 6.1 Principal findings

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

### 6.2 Comparison with existing resources

Several established biomedical knowledge graphs cover subsets of NuGeMi-KG's
content. PrimeKG (Chandak et al. 2023) integrates twenty primary biomedical
resources to describe over 17,000 diseases, but does not include food
composition or microbiome data; cross-layer queries of the form expressible
in NuGeMi-KG are therefore not supported. The Monarch Initiative knowledge
graph (Putman et al. 2024) provides extensive disease–gene–phenotype
integration across species and shares NuGeMi-KG's Biolink alignment, but
similarly lacks both nutritional and microbial layers. Microbe-centric
resources such as KGMicrobe capture microbe–disease
associations without GWAS-level genetic evidence, while food-chemistry
resources such as FooDB and the Virtual Metabolic Human (VMH) catalogue
food composition without linking it to host genetic variation.
NuGeMi-KG's contribution is therefore not the volume of data — at 55,263
nodes it is two orders of magnitude smaller than PrimeKG — but the
structural property that a single five-hop query can traverse all three
biological dimensions simultaneously.

### 6.3 Methodological insights

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

### 6.4 Limitations

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

### 6.5 Implications and future work

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
