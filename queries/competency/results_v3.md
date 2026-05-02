Running 15 competency queries
================================================================================

### cq01_tcf7l2_pleiotropy [PASS]
Q: Which cardiometabolic SNPs map to TCF7L2 and their effect sizes?
Result: 10 rows in 379.0 ms
   {'snp': 'rs34872471', 'disease': 'hyperglycemia', 'effect_size': 0.1397, 'p_value': 1e-323, 'pmid...
   {'snp': 'rs35519679', 'disease': 'type 2 diabetes mellitus', 'effect_size': None, 'p_value': 2e-2...
   {'snp': 'rs34872471', 'disease': 'type 2 diabetes mellitus', 'effect_size': 1.4231888, 'p_value':...
   ... (7 more rows)

### cq02_highest_fiber_foods [PASS]
Q: Which foods have the highest total dietary fiber content?
Result: 10 rows in 114.2 ms
   {'food': 'Flour, coconut', 'fiber_g_per_100g': 34.24, 'unit': 'G'}
   {'food': 'Flaxseed, ground', 'fiber_g_per_100g': 23.13, 'unit': 'G'}
   {'food': 'Flour, rye', 'fiber_g_per_100g': 13.68, 'unit': 'G'}
   ... (7 more rows)

### cq03_butyrate_producers [PASS]
Q: Which gut microbes are known to produce butyrate or other short-chain fatty acids?
Result: 20 rows in 194.9 ms
   {'microbe': 'Christensenella minuta', 'metabolite': 'Butyrate', 'chebi': 'CHEBI:17968'}
   {'microbe': 'Christensenella minuta', 'metabolite': 'Acetate', 'chebi': 'CHEBI:30089'}
   {'microbe': '[Clostridium] scindens', 'metabolite': 'Acetate', 'chebi': 'CHEBI:30089'}
   ... (17 more rows)

### cq04_top_cardiometabolic_genes [PASS]
Q: Which genes carry the most cardiometabolic GWAS signals?
Result: 15 rows in 254.1 ms
   {'gene': 'ADAMTSL3', 'n_snps': 75}
   {'gene': 'LPL', 'n_snps': 71}
   {'gene': 'FAM101A', 'n_snps': 67}
   ... (12 more rows)

### cq05_phenotype_coverage [PASS]
Q: How many SNPs are associated with each cardiometabolic phenotype?
Result: 11 rows in 77.7 ms
   {'phenotype': 'obesity disorder', 'n_snps': 21521}
   {'phenotype': 'hypertensive disorder', 'n_snps': 9276}
   {'phenotype': 'hypercholesterolemia', 'n_snps': 6331}
   ... (8 more rows)

### cq06_foods_via_microbe_nutrient_obesity [EMPTY]
Q: Which foods contain nutrients also produced by obesity-associated microbes?
Result: 0 rows in 147.0 ms

### cq07_microbes_modulating_gwas_genes [PASS]
Q: Which gut microbes modulate host genes that also carry cardiometabolic GWAS variants?
Result: 15 rows in 104.1 ms
   {'microbe': 'Enterococcus faecalis', 'gene': 'PPARG', 'phenotypes': ['obesity disorder', 'type 2 ...
   {'microbe': 'Streptococcus salivarius', 'gene': 'PPARG', 'phenotypes': ['obesity disorder', 'type...
   {'microbe': 'Lactiplantibacillus plantarum', 'gene': 'VEGFA', 'phenotypes': ['hypercholesterolemi...
   ... (12 more rows)

### cq08_t2d_associated_microbes [PASS]
Q: Which gut microbes are directly associated with type 2 diabetes?
Result: 1 rows in 42.5 ms
   {'microbe': 'Faecalibacterium prausnitzii', 'rank': 'species', 'evidence': 'causally'}

### cq09_food_microbe_shared_metabolites [PASS]
Q: Which metabolites are produced by both foods and gut microbes?
Result: 1 rows in 118.8 ms
   {'shared_metabolite': 'Vitamin C, total ascorbic acid', 'n_foods': 78, 'n_microbes': 1, 'example_...

### cq10_tcf7l2_pleiotropy_extended [PASS]
Q: How many distinct cardiometabolic phenotypes does each TCF7L2 SNP touch?
Result: 10 rows in 79.6 ms
   {'snp': 'rs7903146', 'n_phenotypes': 7, 'phenotypes': ['obesity disorder', 'coronary artery disea...
   {'snp': 'rs34872471', 'n_phenotypes': 4, 'phenotypes': ['hyperglycemia', 'type 2 diabetes mellitu...
   {'snp': 'rs4506565', 'n_phenotypes': 3, 'phenotypes': ['hyperglycemia', 'type 2 diabetes mellitus...
   ... (7 more rows)

### cq11_full_five_hop_path [PASS]
Q: Is there a full Food -> Nutrient <- Microbe -> Gene <- SNP -> Phenotype path? (tri-layer)
Result: 10 rows in 118.3 ms
   {'food': 'Potatoes, gold, without skin, raw', 'nutrient': 'Vitamin C, total ascorbic acid', 'micr...
   {'food': 'Restaurant, Chinese, sweet and sour pork', 'nutrient': 'Vitamin C, total ascorbic acid'...
   {'food': 'Cherries, sweet, dark red, raw', 'nutrient': 'Vitamin C, total ascorbic acid', 'microbe...
   ... (7 more rows)

### cq12_pparg_tri_layer_convergence [PASS]
Q: Which microbes and SNPs converge on PPARG — a drug target for cardiometabolic disease?
Result: 2 rows in 86.4 ms
   {'microbe': 'Enterococcus faecalis', 'example_snps': ['rs13059198', 'rs1899951', 'rs4684104', 'rs...
   {'microbe': 'Streptococcus salivarius', 'example_snps': ['rs13059198', 'rs1899951', 'rs4684104', ...

### cq13_bridge_genes_across_layers [PASS]
Q: Which host genes are supported by both gut-microbe modulation AND cardiometabolic GWAS?
Result: 10 rows in 132.2 ms
   {'bridge_gene': 'PPARG', 'phenotype': 'obesity disorder', 'n_microbes': 2, 'n_snps': 39}
   {'bridge_gene': 'VEGFA', 'phenotype': 'obesity disorder', 'n_microbes': 1, 'n_snps': 16}
   {'bridge_gene': 'PPARG', 'phenotype': 'type 2 diabetes mellitus', 'n_microbes': 2, 'n_snps': 12}
   ... (7 more rows)

### cq14_scfa_producers_to_gwas_genes [PASS]
Q: Do SCFA-producing microbes reach obesity/T2D via host-gene modulation?
Result: 10 rows in 198.7 ms
   {'microbe': 'Streptococcus salivarius', 'scfa': 'Butyrate', 'gene': 'PPARG', 'phenotype': 'obesit...
   {'microbe': 'Streptococcus salivarius', 'scfa': 'Butyrate', 'gene': 'PPARG', 'phenotype': 'type 2...
   {'microbe': 'Bifidobacterium longum', 'scfa': 'Acetate', 'gene': 'CYP7A1', 'phenotype': 'obesity ...
   ... (7 more rows)

### cq15_evidence_density_by_phenotype [PASS]
Q: Which cardiometabolic phenotype has the densest tri-layer evidence?
Result: 10 rows in 80.4 ms
   {'phenotype': 'obesity disorder', 'supporting_microbes': 24, 'supporting_genes': 18, 'supporting_...
   {'phenotype': 'hypertriglyceridemia', 'supporting_microbes': 9, 'supporting_genes': 10, 'supporti...
   {'phenotype': 'hypercholesterolemia', 'supporting_microbes': 9, 'supporting_genes': 9, 'supportin...
   ... (7 more rows)

================================================================================
Done. Report written to queries/competency/results.md
