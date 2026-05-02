## 4 Data Records

The cardiometabolic knowledge graph and all reproducibility artefacts are
released under CC-BY-4.0 in two coordinated locations: a Git repository at
https://github.com/sthoniyot/cardiometabolic-kg containing source code,
schema configuration, and pipeline scripts; and a Zenodo deposit at
https://doi.org/10.5281/zenodo.PLACEHOLDER containing the pre-built
knowledge graph artefacts that are too large to commit to a Git history
(Table 2). The two are linked: each tagged GitHub release is deposited to Zenodo, ensuring that every released graph version
is associated with both a Git tag and a persistent DOI.

### 4.1 Pre-built knowledge graph (Zenodo)

The Zenodo deposit (DOI: 10.5281/zenodo.PLACEHOLDER) contains three
pre-built artefacts. **`cardiometabolic_kg_v1.0.0.dump`** (~50 MB) is a
Neo4j 5.x database dump that can be loaded directly into a local Neo4j
instance with `neo4j-admin database load --from-path=./
cardiometabolic_kg_v1.0.0.dump neo4j --overwrite-destination`; this is
the recommended starting point for users who want to immediately query
the graph. **`cardiometabolic_kg_v1.0.0_csv.zip`** (~30 MB compressed)
contains the per-node and per-edge CSV files emitted by the BioCypher
pipeline, with one CSV per node type and one per edge type plus their
corresponding header files; this format is suitable for users who wish
to load the graph into a non-Neo4j backend (e.g. ArangoDB, Memgraph) or
who require a database-agnostic intermediate. **`Cardiometabolic-KG_v1.0.0_source.zip`**
(~5 MB) is a snapshot of the GitHub repository at the v1.0.0 tag,
included for archival completeness so that the deposit is fully
self-contained even if the GitHub repository becomes unavailable.

### 4.2 Source code and pipeline (GitHub)

The Git repository contains all source code, schema configuration, and
documentation needed to rebuild the knowledge graph from the upstream
data sources: three adapter modules (`adapters/gwas_adapter.py`,
`adapters/usda_adapter.py`, `adapters/gutmgene_adapter.py`); the
BioCypher schema configuration (`config/schema_config.yaml`); the
build and load pipeline (`scripts/build_kg.py`, `scripts/load_to_neo4j.py`);
the fifteen competency-question Cypher files (`queries/competency/`);
the manual-audit reproducibility scripts (`scripts/select_audit_subset.py`,
`scripts/score_audit.py`); the audit verdicts as a tab-separated file
(`audit/edge_sample_25.tsv`); pinned dependencies (`requirements.txt`);
project documentation (`README.md`, `DATA_SOURCES.md`, `CHANGELOG.md`);
machine-readable citation metadata (`CITATION.cff`); and the licence
(`LICENSE`). Source data are not included in the repository owing to
file-size and licensing considerations; download instructions and
canonical URLs are documented in `DATA_SOURCES.md`.

### 4.3 Versioning policy

Releases follow semantic versioning (https://semver.org/). Major version
increments (v2.0, v3.0, …) signal schema-breaking changes that affect
existing queries. Minor version increments (v1.1, v1.2, …) signal data
updates from upstream sources or non-breaking schema extensions (e.g.
adding new edge properties). Patch increments (v1.0.1, v1.0.2, …)
signal bug fixes and documentation improvements that do not affect
graph contents. The audit verdict file is regenerated at each minor or
major release and a new audit summary is appended to `CHANGELOG.md`.
