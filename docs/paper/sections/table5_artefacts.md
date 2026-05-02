**Table 5.** Released artefacts. Sizes are approximate at v1.0.0 and may
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
