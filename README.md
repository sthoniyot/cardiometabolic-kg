# Cardiometabolic Knowledge Graph

A tri-layer knowledge graph integrating **nutrigenetics**, **gut microbiome**, and **food chemistry** for precision nutrition in cardiometabolic diseases (type 2 diabetes, obesity, cardiovascular disease).

## Status
Phase 2 complete — schema validated, end-to-end pipeline working.

Tri-layer pipeline: BioCypher schema → CSV export → Neo4j load → Cypher queries.

## Stack
- Python 3.11 (conda env: `kg`)
- BioCypher 0.8.0
- Neo4j 5.x
- Biolink model (via BioCypher ontology alignment)

## Schema
- **8 node types:** SNP, Gene, Pathway, Microbe, CAZyme, Nutrient, Food, Phenotype
- **9 edge types** connecting genetics, microbiome, food, and clinical phenotype layers

## Reproducing
```bash
conda activate kg
python scripts/test_schema.py      # smoke test
python scripts/load_to_neo4j.py    # load into running Neo4j
```

## License
CC-BY-4.0 (applied at v1.0 release)
