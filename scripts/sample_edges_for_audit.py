"""
Stratified random sample of edges for manual audit.

Pulls N edges from each of the four most novel edge types in the KG, with the
provenance fields needed for PubMed verification (PMID, effect size, p-value,
evidence tier).

Output: audit/edge_sample.tsv  (open in Excel/Google Sheets, fill 'verdict' column)
"""
import csv
import random
from pathlib import Path
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password456")
OUT = Path("audit/edge_sample.tsv")
OUT.parent.mkdir(parents=True, exist_ok=True)

# How many edges per type. 50 each = 200 total.
# In practice we audit ~12-15 per type (50 in total) — but we sample more so
# you can skip ones with bad PMIDs and still hit your target.
SAMPLE_PER_TYPE = 50

# (edge type, source label, target label, source props, target props, edge props)
EDGE_QUERIES = {
    "SnpToPhenotype": """
        MATCH (s:Snp)-[r:SnpToPhenotype]->(p:Phenotype)
        WHERE r.pmid IS NOT NULL AND r.pmid <> ''
        RETURN
          s.id AS source_id, s.chromosome AS source_chr,
          p.name AS target_name,
          r.effect_size AS effect_size, r.p_value AS p_value, r.pmid AS pmid
        , rand() AS r ORDER BY r LIMIT $n
    """,
    "FoodToNutrient": """
        MATCH (f:Food)-[r:FoodToNutrient]->(n:Nutrient)
        RETURN
          f.id AS source_id, f.name AS source_name,
          n.id AS target_id, n.name AS target_name,
          r.concentration AS amount, r.unit AS unit,
          '' AS pmid
        , rand() AS r ORDER BY r LIMIT $n
    """,
    "MicrobeToNutrient": """
        MATCH (m:Microbe)-[r:MicrobeToNutrient]->(n:Nutrient)
        RETURN
          m.id AS source_id, m.name AS source_name,
          n.id AS target_id, n.name AS target_name,
          r.evidence_tier AS evidence, r.pmid AS pmid, r.condition AS condition
        , rand() AS rr ORDER BY rr LIMIT $n
    """,
    "MicrobeToGene": """
        MATCH (m:Microbe)-[r:MicrobeToGene]->(g:Gene)
        RETURN
          m.id AS source_id, m.name AS source_name,
          g.symbol AS target_symbol,
          r.evidence_tier AS evidence, r.pmid AS pmid
        , rand() AS rr ORDER BY rr LIMIT $n
    """,
}


def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    rows = []
    with driver.session() as session:
        for edge_type, cypher in EDGE_QUERIES.items():
            print(f"Sampling {SAMPLE_PER_TYPE} {edge_type} edges...")
            res = session.run(cypher, n=SAMPLE_PER_TYPE)
            for rec in res:
                d = dict(rec)
                d.pop("r", None); d.pop("rr", None)
                d["edge_type"] = edge_type
                d["verdict"] = ""        # to fill manually: VERIFIED / PARTIAL / UNVERIFIED / NA
                d["audit_notes"] = ""    # free-text notes
                rows.append(d)
    driver.close()

    # Common columns first, others after
    common = ["edge_type", "source_id", "source_name", "source_chr",
              "target_id", "target_name", "target_symbol",
              "effect_size", "p_value", "amount", "unit",
              "evidence", "condition", "pmid",
              "verdict", "audit_notes"]
    seen_cols = set()
    for row in rows:
        seen_cols.update(row.keys())
    cols = [c for c in common if c in seen_cols] + \
           sorted(c for c in seen_cols if c not in common)

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\n✓ Wrote {len(rows)} edges to {OUT}")
    print(f"  Edge types: {sorted(set(r['edge_type'] for r in rows))}")
    print(f"\nNext: open {OUT} in Excel/Sheets, fill in the 'verdict' column.")
    print("       Then run: python scripts/score_audit.py")


if __name__ == "__main__":
    main()
