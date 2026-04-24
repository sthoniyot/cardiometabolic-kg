"""
Targeted data quality fixes, run against Neo4j directly.
  1. Delete the spurious 'NA' gene node and its edges
  2. Deduplicate MicrobeToNutrient edges (merge PMIDs into a list)
  3. Report on current data quality
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password456")
driver = GraphDatabase.driver(URI, auth=AUTH)


def run(session, cypher, **params):
    result = session.run(cypher, **params)
    return result.consume().counters


def main():
    with driver.session() as session:
        # 1. Remove spurious NA gene
        c = run(session, """
            MATCH (g:Gene {symbol: "NA"})
            DETACH DELETE g
        """)
        print(f"Removed 'NA' gene: {c.nodes_deleted} node, {c.relationships_deleted} edges")

        # Also remove any other non-symbol gene entries
        c = run(session, """
            MATCH (g:Gene)
            WHERE g.symbol IS NULL OR g.symbol IN ["NA", "", "intergenic", "-", "NR"]
            DETACH DELETE g
        """)
        print(f"Removed junk gene symbols: {c.nodes_deleted} nodes, {c.relationships_deleted} edges")

        # 2. Deduplicate MicrobeToNutrient edges
        #    Keep one edge per (source, target), concatenating all PMIDs
        c = run(session, """
            MATCH (m:Microbe)-[r:MicrobeToNutrient]->(n:Nutrient)
            WITH m, n, collect(r) AS rels, collect(DISTINCT r.pmid) AS pmids
            WHERE size(rels) > 1
            WITH m, n, rels, pmids, rels[0] AS keep
            FOREACH (rel IN rels[1..] | DELETE rel)
            SET keep.pmids = [p IN pmids WHERE p <> ''],
                keep.evidence_count = size(pmids)
            REMOVE keep.pmid
        """)
        print(f"MicrobeToNutrient dedup: {c.relationships_deleted} duplicate edges removed")

        # 3. Same for MicrobeToGene
        c = run(session, """
            MATCH (m:Microbe)-[r:MicrobeToGene]->(g:Gene)
            WITH m, g, collect(r) AS rels, collect(DISTINCT r.pmid) AS pmids
            WHERE size(rels) > 1
            WITH m, g, rels, pmids, rels[0] AS keep
            FOREACH (rel IN rels[1..] | DELETE rel)
            SET keep.pmids = [p IN pmids WHERE p <> ''],
                keep.evidence_count = size(pmids)
            REMOVE keep.pmid
        """)
        print(f"MicrobeToGene dedup: {c.relationships_deleted} duplicate edges removed")

        # 4. Final node/edge counts
        n = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        e = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        print(f"\nFinal counts: {n} nodes, {e} edges")

    driver.close()
    print("\n✓ Data-quality fixes applied.")


if __name__ == "__main__":
    main()
