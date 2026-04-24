// Do SCFA-producing microbes reach obesity/T2D via host-gene modulation?
//
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
LIMIT 10;
