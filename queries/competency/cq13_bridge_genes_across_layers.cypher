// Which host genes are supported by both gut-microbe modulation AND cardiometabolic GWAS?
//
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
LIMIT 10;
