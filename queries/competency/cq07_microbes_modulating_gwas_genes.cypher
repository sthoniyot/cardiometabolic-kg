// Which gut microbes modulate host genes that also carry cardiometabolic GWAS variants?
//
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene)
      <-[:SnpToGene]-(s:Snp)
      -[:SnpToPhenotype]->(p:Phenotype)
RETURN m.name AS microbe,
       g.symbol AS gene,
       collect(DISTINCT p.name) AS phenotypes,
       count(DISTINCT s) AS n_snps
ORDER BY n_snps DESC
LIMIT 15;
