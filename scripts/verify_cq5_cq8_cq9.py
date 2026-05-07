"""
Verify the pass/fail status claimed in Table 3 for CQ5, CQ8, and CQ9
by running each query against the Neo4j database and reporting the result.

Usage:
    python scripts/verify_cq5_cq8_cq9.py

Requires the same Neo4j connection settings as the existing build pipeline
(reads from environment variables NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD,
falling back to the defaults that match config/biocypher_config.yaml).
"""
import os
import sys
from neo4j import GraphDatabase


# --------------------------------------------------------------
# Connection settings (override via env vars if needed)
# --------------------------------------------------------------
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password456")  # adjust to your local pw

# --------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------
def banner(text):
    line = "=" * 78
    print()
    print(line)
    print(f"  {text}")
    print(line)


def section(text):
    print()
    print(f"--- {text} ---")


def run(session, query, label=None):
    if label:
        print(f"\n[Query: {label}]")
    print(query.strip())
    print()
    result = session.run(query)
    rows = list(result)
    if not rows:
        print("(no rows returned)")
        return rows
    # Print as a simple table
    keys = rows[0].keys()
    # Compute column widths
    col_w = {k: max(len(str(k)), max((len(str(r[k])) for r in rows), default=0)) for k in keys}
    header = " | ".join(str(k).ljust(col_w[k]) for k in keys)
    print(header)
    print("-" * len(header))
    for r in rows:
        print(" | ".join(str(r[k]).ljust(col_w[k]) for k in keys))
    print(f"\n[{len(rows)} row(s)]")
    return rows


# --------------------------------------------------------------
# Main verification block
# --------------------------------------------------------------
def main():
    print(f"Connecting to Neo4j at {NEO4J_URI} as user {NEO4J_USER!r}...")
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity()
    except Exception as e:
        print(f"ERROR: could not connect to Neo4j: {e}")
        print("If your password differs from the default, set NEO4J_PASSWORD in env.")
        sys.exit(1)
    print("Connected.\n")

    with driver.session() as s:
        # ============================================================
        # CQ5  Foods richest in vitamin C
        # ============================================================
        banner("CQ5  Foods richest in vitamin C")

        section("CQ5.A  Locate vitamin-C nutrient node(s) in the KG")
        run(s, """
            MATCH (n:Nutrient)
            WHERE toLower(n.name) CONTAINS 'ascorbic'
               OR toLower(n.name) CONTAINS 'vitamin c'
               OR n.id IN ['CHEBI:29073', 'CHEBI:38290', 'USDA:401']
            RETURN n.id AS nutrient_id, n.name AS nutrient_name, n.preferred_id AS preferred_id
        """, label="CQ5.A locate vitamin-C nutrient")

        section("CQ5.B  Top 10 foods by vitamin C content")
        run(s, """
            MATCH (f:Food)-[r:FoodToNutrient]->(n:Nutrient)
            WHERE n.id = 'CHEBI:29073'
               OR toLower(n.name) CONTAINS 'ascorbic'
               OR toLower(n.name) CONTAINS 'vitamin c'
            RETURN n.name AS nutrient_name,
                   f.name AS food,
                   r.concentration AS concentration,
                   r.unit AS unit
            ORDER BY r.concentration DESC
            LIMIT 10
        """, label="CQ5.B top foods by vitamin C")

        # ============================================================
        # CQ8  Foods richest in nutrients targeted by gut microbes
        # ============================================================
        banner("CQ8  Foods richest in nutrients targeted by gut microbes")

        section("CQ8.A  Cross-layer nutrient identifier overlap diagnostic")
        run(s, """
            MATCH (n:Nutrient)<-[:MicrobeToNutrient]-(:Microbe)
            WITH collect(DISTINCT n.id) AS mic_nutrients
            MATCH (n:Nutrient)<-[:FoodToNutrient]-(:Food)
            WITH mic_nutrients, collect(DISTINCT n.id) AS food_nutrients
            RETURN size(mic_nutrients) AS microbe_targeted_nutrients,
                   size(food_nutrients) AS food_nutrients,
                   size([x IN mic_nutrients WHERE x IN food_nutrients]) AS overlap
        """, label="CQ8.A nutrient-ID overlap")

        section("CQ8.B  Top 15 (nutrient, food) pairs joined across layers")
        run(s, """
            MATCH (m:Microbe)-[:MicrobeToNutrient]->(n:Nutrient)<-[r:FoodToNutrient]-(f:Food)
            WITH n, f, r.concentration AS food_amount, count(DISTINCT m) AS n_microbes
            WHERE n_microbes > 0
            RETURN n.name AS nutrient,
                   n_microbes AS modulating_microbes,
                   f.name AS food,
                   food_amount AS amount_per_100g
            ORDER BY n_microbes DESC, food_amount DESC
            LIMIT 15
        """, label="CQ8.B top nutrient-food pairs")

        # ============================================================
        # CQ9  SNPs in genes implicated by microbial modulation
        # ============================================================
        banner("CQ9  SNPs in genes implicated by microbial modulation")

        section("CQ9.A  Gene identifier overlap diagnostic (microbiome vs GWAS layers)")
        run(s, """
            MATCH (g:Gene)<-[:MicrobeToGene]-(:Microbe)
            WITH collect(DISTINCT g.id) AS mic_genes
            MATCH (g:Gene)<-[:SnpToGene]-(:Snp)
            WITH mic_genes, collect(DISTINCT g.id) AS gwas_genes
            RETURN size(mic_genes) AS microbe_targeted_genes,
                   size(gwas_genes) AS gwas_genes,
                   size([x IN mic_genes WHERE x IN gwas_genes]) AS overlap
        """, label="CQ9.A gene-ID overlap")

        section("CQ9.B  Top 15 genes ranked by joint microbial+GWAS evidence")
        run(s, """
            MATCH (s:Snp)-[:SnpToGene]->(g:Gene)<-[:MicrobeToGene]-(m:Microbe)
            WITH g, count(DISTINCT s) AS n_snps_in_gene, collect(DISTINCT m.name) AS modulators
            RETURN g.symbol AS gene,
                   n_snps_in_gene,
                   size(modulators) AS n_microbes,
                   modulators
            ORDER BY n_snps_in_gene DESC, n_microbes DESC
            LIMIT 15
        """, label="CQ9.B top tri-layer bridge genes")

        section("CQ9.C  Verify Figure 3 PPARG hub claim (45 SNPs, 2 microbes)")
        run(s, """
            MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: 'PPARG'})<-[:MicrobeToGene]-(m:Microbe)
            RETURN count(DISTINCT s) AS n_snps,
                   count(DISTINCT m) AS n_microbes,
                   collect(DISTINCT m.name) AS microbes
        """, label="CQ9.C PPARG hub")

        # ============================================================
        # Bonus: KG headline statistics (sanity-check the abstract)
        # ============================================================
        banner("Bonus  KG headline statistics (matches abstract claims?)")

        section("Total nodes and edges")
        run(s, """
            MATCH (n) WITH count(n) AS total_nodes
            MATCH ()-[r]->() RETURN total_nodes, count(r) AS total_edges
        """, label="totals")

        section("Per-node-type counts")
        run(s, """
            MATCH (n) RETURN labels(n)[0] AS node_type, count(n) AS n
            ORDER BY n DESC
        """, label="node-type counts")

    driver.close()
    print()
    print("Verification complete.")


if __name__ == "__main__":
    main()
