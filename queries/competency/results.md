# Competency Question Results

_Generated: 2026-04-29T18:02:44.965530_  
_KG: Neo4j at bolt://localhost:7687_

## Summary

| Query | Status | Rows | Time (ms) |
|---|---|---|---|
| cq01_tcf7l2_pleiotropy | PASS | 10 | 379.0 |
| cq02_highest_fiber_foods | PASS | 10 | 114.2 |
| cq03_butyrate_producers | PASS | 20 | 194.9 |
| cq04_top_cardiometabolic_genes | PASS | 15 | 254.1 |
| cq05_phenotype_coverage | PASS | 11 | 77.7 |
| cq06_foods_via_microbe_nutrient_obesity | EMPTY | 0 | 147.0 |
| cq07_microbes_modulating_gwas_genes | PASS | 15 | 104.1 |
| cq08_t2d_associated_microbes | PASS | 1 | 42.5 |
| cq09_food_microbe_shared_metabolites | PASS | 1 | 118.8 |
| cq10_tcf7l2_pleiotropy_extended | PASS | 10 | 79.6 |
| cq11_full_five_hop_path | PASS | 10 | 118.3 |
| cq12_pparg_tri_layer_convergence | PASS | 2 | 86.4 |
| cq13_bridge_genes_across_layers | PASS | 10 | 132.2 |
| cq14_scfa_producers_to_gwas_genes | PASS | 10 | 198.7 |
| cq15_evidence_density_by_phenotype | PASS | 10 | 80.4 |

---

## cq01_tcf7l2_pleiotropy  `[PASS]`
**Question:** Which cardiometabolic SNPs map to TCF7L2 and their effect sizes?

**Rows:** 10 · **Time:** 379.0 ms

```cypher
MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})

MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)

RETURN s.id AS snp,

       p.name AS disease,

       r.effect_size AS effect_size,

       r.p_value AS p_value,

       r.pmid AS pmid

ORDER BY r.p_value

LIMIT 10
```

**Example rows (first 5):**

```json
{"snp": "rs34872471", "disease": "hyperglycemia", "effect_size": 0.1397, "p_value": 1e-323, "pmid": "39024449"}
{"snp": "rs35519679", "disease": "type 2 diabetes mellitus", "effect_size": null, "p_value": 2e-218, "pmid": "38062574"}
{"snp": "rs34872471", "disease": "type 2 diabetes mellitus", "effect_size": 1.4231888, "p_value": 1e-94, "pmid": "29358691"}
{"snp": "rs7901695", "disease": "type 2 diabetes mellitus", "effect_size": 1.3568672, "p_value": 7e-52, "pmid": "32514122"}
{"snp": "rs4506565", "disease": "hyperglycemia", "effect_size": 0.021991, "p_value": 8e-24, "pmid": "33402679"}
```

_(5 additional rows not shown)_

## cq02_highest_fiber_foods  `[PASS]`
**Question:** Which foods have the highest total dietary fiber content?

**Rows:** 10 · **Time:** 114.2 ms

```cypher
MATCH (f:Food)-[r:FoodToNutrient]->(n:Nutrient {name: "Fiber, total dietary"})

RETURN f.name AS food,

       r.concentration AS fiber_g_per_100g,

       r.unit AS unit

ORDER BY r.concentration DESC

LIMIT 10
```

**Example rows (first 5):**

```json
{"food": "Flour, coconut", "fiber_g_per_100g": 34.24, "unit": "G"}
{"food": "Flaxseed, ground", "fiber_g_per_100g": 23.13, "unit": "G"}
{"food": "Flour, rye", "fiber_g_per_100g": 13.68, "unit": "G"}
{"food": "Flour, barley", "fiber_g_per_100g": 12.79, "unit": "G"}
{"food": "Nuts, almonds, dry roasted, with salt added", "fiber_g_per_100g": 11.0, "unit": "G"}
```

_(5 additional rows not shown)_

## cq03_butyrate_producers  `[PASS]`
**Question:** Which gut microbes are known to produce butyrate or other short-chain fatty acids?

**Rows:** 20 · **Time:** 194.9 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToNutrient]->(n:Nutrient)

WHERE toLower(n.name) CONTAINS "butyr"

   OR toLower(n.name) CONTAINS "propion"

   OR toLower(n.name) CONTAINS "acetate"

RETURN m.name AS microbe,

       n.name AS metabolite,

       n.id AS chebi

LIMIT 20
```

**Example rows (first 5):**

```json
{"microbe": "Christensenella minuta", "metabolite": "Butyrate", "chebi": "CHEBI:17968"}
{"microbe": "Christensenella minuta", "metabolite": "Acetate", "chebi": "CHEBI:30089"}
{"microbe": "[Clostridium] scindens", "metabolite": "Acetate", "chebi": "CHEBI:30089"}
{"microbe": "Bifidobacterium", "metabolite": "Acetate", "chebi": "CHEBI:30089"}
{"microbe": "Eubacterium ramulus", "metabolite": "Butyrate", "chebi": "CHEBI:17968"}
```

_(15 additional rows not shown)_

## cq04_top_cardiometabolic_genes  `[PASS]`
**Question:** Which genes carry the most cardiometabolic GWAS signals?

**Rows:** 15 · **Time:** 254.1 ms

```cypher
MATCH (s:Snp)-[:SnpToGene]->(g:Gene)

RETURN g.symbol AS gene,

       count(DISTINCT s) AS n_snps

ORDER BY n_snps DESC

LIMIT 15
```

**Example rows (first 5):**

```json
{"gene": "ADAMTSL3", "n_snps": 75}
{"gene": "LPL", "n_snps": 71}
{"gene": "FAM101A", "n_snps": 67}
{"gene": "RSPO3", "n_snps": 58}
{"gene": "DLEU1", "n_snps": 53}
```

_(10 additional rows not shown)_

## cq05_phenotype_coverage  `[PASS]`
**Question:** How many SNPs are associated with each cardiometabolic phenotype?

**Rows:** 11 · **Time:** 77.7 ms

```cypher
MATCH (s:Snp)-[:SnpToPhenotype]->(p:Phenotype)

RETURN p.name AS phenotype,

       count(DISTINCT s) AS n_snps

ORDER BY n_snps DESC
```

**Example rows (first 5):**

```json
{"phenotype": "obesity disorder", "n_snps": 21521}
{"phenotype": "hypertensive disorder", "n_snps": 9276}
{"phenotype": "hypercholesterolemia", "n_snps": 6331}
{"phenotype": "hypertriglyceridemia", "n_snps": 5959}
{"phenotype": "type 2 diabetes mellitus", "n_snps": 4890}
```

_(6 additional rows not shown)_

## cq06_foods_via_microbe_nutrient_obesity  `[EMPTY]`
**Question:** Which foods contain nutrients also produced by obesity-associated microbes?

**Rows:** 0 · **Time:** 147.0 ms

```cypher
MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)

      <-[:MicrobeToNutrient]-(m:Microbe)

      -[:MicrobeToPhenotype]->(p:Phenotype {name: "obesity disorder"})

RETURN f.name AS food,

       n.name AS shared_nutrient,

       collect(DISTINCT m.name) AS obesity_microbes

LIMIT 10
```

_No rows returned._

## cq07_microbes_modulating_gwas_genes  `[PASS]`
**Question:** Which gut microbes modulate host genes that also carry cardiometabolic GWAS variants?

**Rows:** 15 · **Time:** 104.1 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene)

      <-[:SnpToGene]-(s:Snp)

      -[:SnpToPhenotype]->(p:Phenotype)

RETURN m.name AS microbe,

       g.symbol AS gene,

       collect(DISTINCT p.name) AS phenotypes,

       count(DISTINCT s) AS n_snps

ORDER BY n_snps DESC

LIMIT 15
```

**Example rows (first 5):**

```json
{"microbe": "Enterococcus faecalis", "gene": "PPARG", "phenotypes": ["obesity disorder", "type 2 diabetes mellitus", "hypercholesterolemia", "hypertriglyceridemia", "hypertensive disorder", "metabolic syndrome", "hyperglycemia"], "n_snps": 45}
{"microbe": "Streptococcus salivarius", "gene": "PPARG", "phenotypes": ["obesity disorder", "type 2 diabetes mellitus", "hypercholesterolemia", "hypertriglyceridemia", "hypertensive disorder", "metabolic syndrome", "hyperglycemia"], "n_snps": 45}
{"microbe": "Lactiplantibacillus plantarum", "gene": "VEGFA", "phenotypes": ["hypercholesterolemia", "hypertriglyceridemia", "obesity disorder", "type 2 diabetes mellitus", "metabolic syndrome", "coronary artery disease", "hyperglycemia", "hypertensive disorder", "cardiovascular disorder"], "n_snps": 20}
{"microbe": "Lactiplantibacillus plantarum", "gene": "HNF4A", "phenotypes": ["type 2 diabetes mellitus", "hypercholesterolemia", "hyperglycemia", "metabolic syndrome", "hypertriglyceridemia", "coronary artery disease", "hypertensive disorder"], "n_snps": 9}
{"microbe": "Streptococcus salivarius", "gene": "ANGPTL4", "phenotypes": ["metabolic syndrome", "hypertriglyceridemia", "obesity disorder", "coronary artery disease", "type 2 diabetes mellitus", "hypercholesterolemia"], "n_snps": 8}
```

_(10 additional rows not shown)_

## cq08_t2d_associated_microbes  `[PASS]`
**Question:** Which gut microbes are directly associated with type 2 diabetes?

**Rows:** 1 · **Time:** 42.5 ms

```cypher
MATCH (m:Microbe)-[r:MicrobeToPhenotype]->(p:Phenotype {name: "type 2 diabetes mellitus"})

RETURN m.name AS microbe,

       m.rank AS rank,

       r.evidence_tier AS evidence
```

**Example rows (first 5):**

```json
{"microbe": "Faecalibacterium prausnitzii", "rank": "species", "evidence": "causally"}
```

## cq09_food_microbe_shared_metabolites  `[PASS]`
**Question:** Which metabolites are produced by both foods and gut microbes?

**Rows:** 1 · **Time:** 118.8 ms

```cypher
MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)

      <-[:MicrobeToNutrient]-(m:Microbe)

RETURN n.name AS shared_metabolite,

       count(DISTINCT f) AS n_foods,

       count(DISTINCT m) AS n_microbes,

       collect(DISTINCT f.name)[..3] AS example_foods,

       collect(DISTINCT m.name)[..3] AS example_microbes

ORDER BY n_foods DESC
```

**Example rows (first 5):**

```json
{"shared_metabolite": "Vitamin C, total ascorbic acid", "n_foods": 78, "n_microbes": 1, "example_foods": ["Potatoes, gold, without skin, raw", "Restaurant, Chinese, sweet and sour pork", "Cherries, sweet, dark red, raw"], "example_microbes": ["Lactiplantibacillus plantarum"]}
```

## cq10_tcf7l2_pleiotropy_extended  `[PASS]`
**Question:** How many distinct cardiometabolic phenotypes does each TCF7L2 SNP touch?

**Rows:** 10 · **Time:** 79.6 ms

```cypher
MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})

MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)

RETURN s.id AS snp,

       count(DISTINCT p) AS n_phenotypes,

       collect(DISTINCT p.name) AS phenotypes

ORDER BY n_phenotypes DESC

LIMIT 10
```

**Example rows (first 5):**

```json
{"snp": "rs7903146", "n_phenotypes": 7, "phenotypes": ["obesity disorder", "coronary artery disease", "hyperglycemia", "hypertriglyceridemia", "hypertensive disorder", "hypercholesterolemia", "type 2 diabetes mellitus"]}
{"snp": "rs34872471", "n_phenotypes": 4, "phenotypes": ["hyperglycemia", "type 2 diabetes mellitus", "hypertensive disorder", "obesity disorder"]}
{"snp": "rs4506565", "n_phenotypes": 3, "phenotypes": ["hyperglycemia", "type 2 diabetes mellitus", "obesity disorder"]}
{"snp": "rs35519679", "n_phenotypes": 3, "phenotypes": ["obesity disorder", "type 2 diabetes mellitus", "hypertensive disorder"]}
{"snp": "rs7896811", "n_phenotypes": 2, "phenotypes": ["metabolic syndrome", "type 2 diabetes mellitus"]}
```

_(5 additional rows not shown)_

## cq11_full_five_hop_path  `[PASS]`
**Question:** Is there a full Food -> Nutrient <- Microbe -> Gene <- SNP -> Phenotype path? (tri-layer)

**Rows:** 10 · **Time:** 118.3 ms

```cypher
MATCH path = (f:Food)-[:FoodToNutrient]->(n:Nutrient)

             <-[:MicrobeToNutrient]-(m:Microbe)

             -[:MicrobeToGene]->(g:Gene)

             <-[:SnpToGene]-(s:Snp)

             -[:SnpToPhenotype]->(p:Phenotype)

RETURN f.name AS food,

       n.name AS nutrient,

       m.name AS microbe,

       g.symbol AS gene,

       s.id AS snp,

       p.name AS phenotype

LIMIT 10
```

**Example rows (first 5):**

```json
{"food": "Potatoes, gold, without skin, raw", "nutrient": "Vitamin C, total ascorbic acid", "microbe": "Lactiplantibacillus plantarum", "gene": "ACTB", "snp": "rs852388", "phenotype": "hypertriglyceridemia"}
{"food": "Restaurant, Chinese, sweet and sour pork", "nutrient": "Vitamin C, total ascorbic acid", "microbe": "Lactiplantibacillus plantarum", "gene": "ACTB", "snp": "rs852388", "phenotype": "hypertriglyceridemia"}
{"food": "Cherries, sweet, dark red, raw", "nutrient": "Vitamin C, total ascorbic acid", "microbe": "Lactiplantibacillus plantarum", "gene": "ACTB", "snp": "rs852388", "phenotype": "hypertriglyceridemia"}
{"food": "Strawberries, raw", "nutrient": "Vitamin C, total ascorbic acid", "microbe": "Lactiplantibacillus plantarum", "gene": "ACTB", "snp": "rs852388", "phenotype": "hypertriglyceridemia"}
{"food": "Grapes, green, seedless, raw", "nutrient": "Vitamin C, total ascorbic acid", "microbe": "Lactiplantibacillus plantarum", "gene": "ACTB", "snp": "rs852388", "phenotype": "hypertriglyceridemia"}
```

_(5 additional rows not shown)_

## cq12_pparg_tri_layer_convergence  `[PASS]`
**Question:** Which microbes and SNPs converge on PPARG — a drug target for cardiometabolic disease?

**Rows:** 2 · **Time:** 86.4 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene {symbol: "PPARG"})

      <-[:SnpToGene]-(s:Snp)

      -[:SnpToPhenotype]->(p:Phenotype)

RETURN m.name AS microbe,

       collect(DISTINCT s.id)[..5] AS example_snps,

       count(DISTINCT s) AS total_snps,

       collect(DISTINCT p.name) AS phenotypes

ORDER BY total_snps DESC
```

**Example rows (first 5):**

```json
{"microbe": "Enterococcus faecalis", "example_snps": ["rs13059198", "rs1899951", "rs4684104", "rs4135300", "rs17819328"], "total_snps": 45, "phenotypes": ["obesity disorder", "type 2 diabetes mellitus", "hypercholesterolemia", "hypertriglyceridemia", "hypertensive disorder", "metabolic syndrome", "hyperglycemia"]}
{"microbe": "Streptococcus salivarius", "example_snps": ["rs13059198", "rs1899951", "rs4684104", "rs4135300", "rs17819328"], "total_snps": 45, "phenotypes": ["obesity disorder", "type 2 diabetes mellitus", "hypercholesterolemia", "hypertriglyceridemia", "hypertensive disorder", "metabolic syndrome", "hyperglycemia"]}
```

## cq13_bridge_genes_across_layers  `[PASS]`
**Question:** Which host genes are supported by both gut-microbe modulation AND cardiometabolic GWAS?

**Rows:** 10 · **Time:** 132.2 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene)

      <-[:SnpToGene]-(s:Snp)

      -[:SnpToPhenotype]->(p:Phenotype)

WITH g, p,

     count(DISTINCT m) AS n_microbes,

     count(DISTINCT s) AS n_snps

WHERE n_microbes >= 1 AND n_snps >= 5

RETURN g.symbol AS bridge_gene,

       p.name AS phenotype,

       n_microbes,

       n_snps

ORDER BY n_snps DESC

LIMIT 10
```

**Example rows (first 5):**

```json
{"bridge_gene": "PPARG", "phenotype": "obesity disorder", "n_microbes": 2, "n_snps": 39}
{"bridge_gene": "VEGFA", "phenotype": "obesity disorder", "n_microbes": 1, "n_snps": 16}
{"bridge_gene": "PPARG", "phenotype": "type 2 diabetes mellitus", "n_microbes": 2, "n_snps": 12}
{"bridge_gene": "VEGFA", "phenotype": "hypertriglyceridemia", "n_microbes": 1, "n_snps": 10}
{"bridge_gene": "PPARG", "phenotype": "hypertriglyceridemia", "n_microbes": 2, "n_snps": 10}
```

_(5 additional rows not shown)_

## cq14_scfa_producers_to_gwas_genes  `[PASS]`
**Question:** Do SCFA-producing microbes reach obesity/T2D via host-gene modulation?

**Rows:** 10 · **Time:** 198.7 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToNutrient]->(n:Nutrient)

WHERE toLower(n.name) CONTAINS "acetate"

   OR toLower(n.name) CONTAINS "propion"

   OR toLower(n.name) CONTAINS "butyr"

MATCH (m)-[:MicrobeToGene]->(g:Gene)

      <-[:SnpToGene]-(s:Snp)

      -[:SnpToPhenotype]->(p:Phenotype)

WHERE p.name IN ["type 2 diabetes mellitus", "obesity disorder"]

RETURN m.name AS microbe,

       n.name AS scfa,

       g.symbol AS gene,

       p.name AS phenotype,

       count(DISTINCT s) AS n_snps

ORDER BY n_snps DESC

LIMIT 10
```

**Example rows (first 5):**

```json
{"microbe": "Streptococcus salivarius", "scfa": "Butyrate", "gene": "PPARG", "phenotype": "obesity disorder", "n_snps": 39}
{"microbe": "Streptococcus salivarius", "scfa": "Butyrate", "gene": "PPARG", "phenotype": "type 2 diabetes mellitus", "n_snps": 12}
{"microbe": "Bifidobacterium longum", "scfa": "Acetate", "gene": "CYP7A1", "phenotype": "obesity disorder", "n_snps": 2}
{"microbe": "Streptococcus salivarius", "scfa": "Butyrate", "gene": "ANGPTL4", "phenotype": "type 2 diabetes mellitus", "n_snps": 2}
{"microbe": "Akkermansia muciniphila", "scfa": "Acetate", "gene": "TLR4", "phenotype": "obesity disorder", "n_snps": 1}
```

_(5 additional rows not shown)_

## cq15_evidence_density_by_phenotype  `[PASS]`
**Question:** Which cardiometabolic phenotype has the densest tri-layer evidence?

**Rows:** 10 · **Time:** 80.4 ms

```cypher
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene)

      <-[:SnpToGene]-(s:Snp)

      -[:SnpToPhenotype]->(p:Phenotype)

WITH p,

     count(DISTINCT m) AS microbes,

     count(DISTINCT g) AS genes,

     count(DISTINCT s) AS snps

RETURN p.name AS phenotype,

       microbes AS supporting_microbes,

       genes AS supporting_genes,

       snps AS supporting_snps,

       microbes * genes * snps AS evidence_density

ORDER BY evidence_density DESC
```

**Example rows (first 5):**

```json
{"phenotype": "obesity disorder", "supporting_microbes": 24, "supporting_genes": 18, "supporting_snps": 81, "evidence_density": 34992}
{"phenotype": "hypertriglyceridemia", "supporting_microbes": 9, "supporting_genes": 10, "supporting_snps": 35, "evidence_density": 3150}
{"phenotype": "hypercholesterolemia", "supporting_microbes": 9, "supporting_genes": 9, "supporting_snps": 36, "evidence_density": 2916}
{"phenotype": "type 2 diabetes mellitus", "supporting_microbes": 8, "supporting_genes": 8, "supporting_snps": 36, "evidence_density": 2304}
{"phenotype": "coronary artery disease", "supporting_microbes": 16, "supporting_genes": 7, "supporting_snps": 12, "evidence_density": 1344}
```

_(5 additional rows not shown)_