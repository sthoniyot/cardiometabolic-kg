from biocypher import BioCypher

bc = BioCypher(
    biocypher_config_path="config/biocypher_config.yaml",
    schema_config_path="config/schema_config.yaml",
)

test_nodes = [
    ("rs7903146", "snp",
        {"chromosome": "10", "position": 112998590, "risk_allele": "T"}),
    ("HGNC:11641", "gene",
        {"symbol": "TCF7L2", "description": "Transcription factor 7 like 2"}),
    ("R-HSA-195721", "pathway",
        {"name": "Signaling by WNT", "source": "Reactome"}),
    ("NCBITaxon:239935", "microbe",
        {"name": "Akkermansia muciniphila", "rank": "species"}),
    ("UniProt:P77791", "cazyme",
        {"family": "GH16", "function": "beta-glucanase", "cazy_family": "GH16"}),
    ("CHEBI:30772", "nutrient",
        {"name": "butyrate", "compound_class": "SCFA"}),
    ("FOODON:03301710", "food",
        {"name": "oats", "food_group": "cereals"}),
    ("MONDO:0005148", "phenotype",
        {"name": "type 2 diabetes", "category": "metabolic"}),
]

test_edges = [
    ("e1", "rs7903146", "HGNC:11641", "snp_to_gene", {}),
    ("e2", "rs7903146", "MONDO:0005148", "snp_to_phenotype",
        {"p_value": 1e-50, "effect_size": 1.37, "pmid": "17463249"}),
    ("e3", "HGNC:11641", "R-HSA-195721", "gene_to_pathway", {}),
    ("e4", "FOODON:03301710", "CHEBI:30772", "food_to_nutrient",
        {"concentration": 0.5, "unit": "mg/g"}),
    ("e5", "NCBITaxon:239935", "CHEBI:30772", "microbe_to_nutrient",
        {"evidence_tier": "moderate"}),
    ("e6", "NCBITaxon:239935", "UniProt:P77791", "microbe_to_cazyme", {}),
    ("e7", "CHEBI:30772", "MONDO:0005148", "nutrient_to_phenotype",
        {"evidence_tier": "strong", "pmid": "25838346"}),
    ("e8", "NCBITaxon:239935", "MONDO:0005148", "microbe_to_phenotype", {}),
]

bc.write_nodes(test_nodes)
bc.write_edges(test_edges)
bc.write_import_call()
bc.summary()
print("\n✓ Schema is valid and BioCypher pipeline works.")
