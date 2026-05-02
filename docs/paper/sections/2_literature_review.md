## 2 Literature Review

The construction of NuGeMi-KG draws on four converging research threads:
nutrigenetics and gene-diet interaction, gut-microbiome contributions to
cardiometabolic disease, food-chemistry ontologies, and biomedical knowledge
graphs as a computational substrate. We briefly summarise the state of each.

### 2.1 Nutrigenetics and gene-diet interaction

Nutrigenetics — the study of how host genetic variation modulates the
response to dietary intake — has matured from candidate-gene associations
to genome-wide investigation of gene-environment (G × E) interaction
[9]. Recent reviews report over 300 G × E loci interacting with metabolic
syndrome traits across 42 GWAS, with FTO, MC4R, TCF7L2, and PPARA
recurring as principal variants [9, 10]. Birk (2025) summarises evidence
that polymorphisms in CYP2R1, TMEM18, and FTO modulate obesity and
metabolic-syndrome risk in a diet-dependent manner [11], while Hossain
et al. (2025) catalogue 127 candidate genes and 253 quantitative trait
loci implicated in obesity susceptibility, distinguishing rare monogenic
variants (LEP, LEPR, MC4R, POMC, PCSK1) from common polygenic loci [12].
Despite this volume of evidence, translation to clinical precision-nutrition
intervention remains limited [13]: the Nature Medicine review by Berry
et al. (2025) explicitly identifies the lack of integration across genetic,
microbial, and dietary data sources as a principal barrier to clinical
deployment [13].

### 2.2 Gut microbiome contributions to cardiometabolic disease

The gut microbiome is now established as an independent contributor to
cardiometabolic risk. The Nature Reviews Cardiology synthesis by Witkowski
et al. (2023) describes specific microbe-derived metabolites — short-chain
fatty acids (acetate, butyrate, propionate), trimethylamine N-oxide
(TMAO), bile-acid derivatives — as causal mediators of host inflammation,
endothelial dysfunction, and insulin resistance [14]. Theofilis et al.
(2024) review microbe-targeted therapeutic options for cardiometabolic
disease, including fecal-microbiota transplantation and dietary modulation
[15]. Carter et al. (2025) report in *Cell* that a non-industrialised-type
diet restores microbiome diversity and enhances *Limosilactobacillus
reuteri* persistence with measurable cardiometabolic benefit [16].
Wei et al. (2025) extend this work to the gut mycobiome, identifying
*Candida* and *Saccharomyces* dysbiosis as cardiometabolic risk factors
[17]. Across these studies, mechanistic hypotheses are typically generated
manually from individual papers; the systematic integration of
microbe-metabolite-host-gene relationships remains, as gutMGene v2.0's
curators note, an active curation challenge [3].

### 2.3 Food-chemistry resources and ontologies

Food-composition databases provide the third layer. USDA FoodData Central
(USDA-FDC) supplies analytical-laboratory measurements for hundreds of
foods across more than 600 nutrients [2]. FooDB catalogues approximately
28,000 chemicals across 1,000 raw or unprocessed foods, including
non-nutrient bioactives [18]. The FoodOn ontology, an OBO-Foundry member,
provides a standardised hierarchy of food product terms reused across
ChEBI for chemical entities, NCBITaxon for source organisms, and ENVO
for environmental context [19]. Built on these foundations, FoodKG
integrates over a million recipes against FoodOn and ChEBI [20], and
FoodAtlas extracts food-chemical relationships from the literature using
LLM-assisted entity resolution [21]. None of these resources, however,
links food composition to host genetic variation or gut microbial activity.

### 2.4 Biomedical knowledge graphs and integration frameworks

Biomedical knowledge graphs (BKGs) have emerged as the principal
computational paradigm for cross-resource integration. Yang et al. (2024)
review healthcare KGs across construction methodology, utilisation
technique, and downstream application, noting the rapid convergence of
KGs with large language models [22]. Lobentanzer et al. (2023) introduce
BioCypher as a FAIR framework that standardises KG construction while
preserving provenance [7]; Chandak et al. (2023) demonstrate the
PrimeKG resource integrating 20 primary biomedical sources to describe
17,080 diseases [4]; Putman et al. (2024) describe the Monarch Initiative
as an analytic platform integrating cross-species disease-gene-phenotype
data under Biolink Model alignment [5]. Recent surveys frame the field
as transitioning from static reference graphs to LLM-grounded reasoning
substrates [22, 23]. Across these efforts, however, food composition and
gut microbial activity have not been jointly integrated with host
nutrigenetics under a single ontology-aligned schema — the gap that
NuGeMi-KG addresses.

### 2.5 Summary of cited literature

The references underpinning this review are summarised in Table 1.
