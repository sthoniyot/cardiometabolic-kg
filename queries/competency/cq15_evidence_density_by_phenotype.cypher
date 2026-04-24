// Which cardiometabolic phenotype has the densest tri-layer evidence?
//
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
ORDER BY evidence_density DESC;
