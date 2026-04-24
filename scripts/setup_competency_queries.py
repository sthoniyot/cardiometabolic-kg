"""
Creates 15 competency question .cypher files in queries/competency/.
Each file holds one query, ready to be run by scripts/run_competency.py
or pasted directly into Neo4j Browser.
"""
import os
from pathlib import Path
from textwrap import dedent

OUT_DIR = Path("queries/competency")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Each entry: (filename, natural-language question, cypher body)
QUERIES = [
    # ─── Tier 1: single-layer sanity (CQ1–CQ5) ─────────────────────────────
    (
        "cq01_tcf7l2_pleiotropy.cypher",
        "Which cardiometabolic SNPs map to TCF7L2 and their effect sizes?",
        """
        MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})
        MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)
        RETURN s.id AS snp,
               p.name AS disease,
               r.effect_size AS effect_size,
               r.p_value AS p_value,
               r.pmid AS pmid
        ORDER BY r.p_value
        LIMIT 10
        """,
    ),
    (
        "cq02_highest_fiber_foods.cypher",
        "Which foods have the highest total dietary fiber content?",
        """
        MATCH (f:Food)-[r:FoodToNutrient]->(n:Nutrient {name: "Fiber, total dietary"})
        RETURN f.name AS food,
               r.concentration AS fiber_g_per_100g,
               r.unit AS unit
        ORDER BY r.concentration DESC
        LIMIT 10
        """,
    ),
    (
        "cq03_butyrate_producers.cypher",
        "Which gut microbes are known to produce butyrate or other short-chain fatty acids?",
        """
        MATCH (m:Microbe)-[:MicrobeToNutrient]->(n:Nutrient)
        WHERE toLower(n.name) CONTAINS "butyr"
           OR toLower(n.name) CONTAINS "propion"
           OR toLower(n.name) CONTAINS "acetate"
        RETURN m.name AS microbe,
               n.name AS metabolite,
               n.id AS chebi
        LIMIT 20
        """,
    ),
    (
        "cq04_top_cardiometabolic_genes.cypher",
        "Which genes carry the most cardiometabolic GWAS signals?",
        """
        MATCH (s:Snp)-[:SnpToGene]->(g:Gene)
        RETURN g.symbol AS gene,
               count(DISTINCT s) AS n_snps
        ORDER BY n_snps DESC
        LIMIT 15
        """,
    ),
    (
        "cq05_phenotype_coverage.cypher",
        "How many SNPs are associated with each cardiometabolic phenotype?",
        """
        MATCH (s:Snp)-[:SnpToPhenotype]->(p:Phenotype)
        RETURN p.name AS phenotype,
               count(DISTINCT s) AS n_snps
        ORDER BY n_snps DESC
        """,
    ),
    # ─── Tier 2: two-layer integration (CQ6–CQ10) ─────────────────────────
    (
        "cq06_foods_via_microbe_nutrient_obesity.cypher",
        "Which foods contain nutrients also produced by obesity-associated microbes?",
        """
        MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)
              <-[:MicrobeToNutrient]-(m:Microbe)
              -[:MicrobeToPhenotype]->(p:Phenotype {name: "obesity disorder"})
        RETURN f.name AS food,
               n.name AS shared_nutrient,
               collect(DISTINCT m.name) AS obesity_microbes
        LIMIT 10
        """,
    ),
    (
        "cq07_microbes_modulating_gwas_genes.cypher",
        "Which gut microbes modulate host genes that also carry cardiometabolic GWAS variants?",
        """
        MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene)
              <-[:SnpToGene]-(s:Snp)
              -[:SnpToPhenotype]->(p:Phenotype)
        RETURN m.name AS microbe,
               g.symbol AS gene,
               collect(DISTINCT p.name) AS phenotypes,
               count(DISTINCT s) AS n_snps
        ORDER BY n_snps DESC
        LIMIT 15
        """,
    ),
    (
        "cq08_t2d_associated_microbes.cypher",
        "Which gut microbes are directly associated with type 2 diabetes?",
        """
        MATCH (m:Microbe)-[r:MicrobeToPhenotype]->(p:Phenotype {name: "type 2 diabetes mellitus"})
        RETURN m.name AS microbe,
               m.rank AS rank,
               r.evidence_tier AS evidence
        """,
    ),
    (
        "cq09_food_microbe_shared_metabolites.cypher",
        "Which metabolites are produced by both foods and gut microbes?",
        """
        MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)
              <-[:MicrobeToNutrient]-(m:Microbe)
        RETURN n.name AS shared_metabolite,
               count(DISTINCT f) AS n_foods,
               count(DISTINCT m) AS n_microbes,
               collect(DISTINCT f.name)[..3] AS example_foods,
               collect(DISTINCT m.name)[..3] AS example_microbes
        ORDER BY n_foods DESC
        """,
    ),
    (
        "cq10_tcf7l2_pleiotropy_extended.cypher",
        "How many distinct cardiometabolic phenotypes does each TCF7L2 SNP touch?",
        """
        MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})
        MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)
        RETURN s.id AS snp,
               count(DISTINCT p) AS n_phenotypes,
               collect(DISTINCT p.name) AS phenotypes
        ORDER BY n_phenotypes DESC
        LIMIT 10
        """,
    ),
    # ─── Tier 3: three-layer novel queries (CQ11–CQ15) ────────────────────
    (
        "cq11_full_five_hop_path.cypher",
        "Is there a full Food -> Nutrient <- Microbe -> Gene <- SNP -> Phenotype path? (tri-layer)",
        """
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
        """,
    ),
    (
        "cq12_pparg_tri_layer_convergence.cypher",
        "Which microbes and SNPs converge on PPARG — a drug target for cardiometabolic disease?",
        """
        MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene {symbol: "PPARG"})
              <-[:SnpToGene]-(s:Snp)
              -[:SnpToPhenotype]->(p:Phenotype)
        RETURN m.name AS microbe,
               collect(DISTINCT s.id)[..5] AS example_snps,
               count(DISTINCT s) AS total_snps,
               collect(DISTINCT p.name) AS phenotypes
        ORDER BY total_snps DESC
        """,
    ),
    (
        "cq13_bridge_genes_across_layers.cypher",
        "Which host genes are supported by both gut-microbe modulation AND cardiometabolic GWAS?",
        """
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
        """,
    ),
    (
        "cq14_scfa_producers_to_gwas_genes.cypher",
        "Do SCFA-producing microbes reach obesity/T2D via host-gene modulation?",
        """
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
        """,
    ),
    (
        "cq15_evidence_density_by_phenotype.cypher",
        "Which cardiometabolic phenotype has the densest tri-layer evidence?",
        """
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
        """,
    ),
]


def write_queries():
    index_lines = ["# Competency questions index\n"]
    for filename, question, cypher in QUERIES:
        path = OUT_DIR / filename
        body = dedent(cypher).strip() + ";\n"
        header = f"// {question}\n//\n"
        with open(path, "w") as f:
            f.write(header)
            f.write(body)
        print(f"Wrote {path}")
        index_lines.append(f"- **{filename.replace('.cypher', '')}** — {question}")

    # also write an index README
    readme = OUT_DIR / "README.md"
    with open(readme, "w") as f:
        f.write("\n".join(index_lines) + "\n")
    print(f"Wrote {readme}")


if __name__ == "__main__":
    write_queries()
    print(f"\n✓ Wrote {len(QUERIES)} competency queries to {OUT_DIR}/")
