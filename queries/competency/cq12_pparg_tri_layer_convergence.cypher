// Which microbes and SNPs converge on PPARG — a drug target for cardiometabolic disease?
//
MATCH (m:Microbe)-[:MicrobeToGene]->(g:Gene {symbol: "PPARG"})
      <-[:SnpToGene]-(s:Snp)
      -[:SnpToPhenotype]->(p:Phenotype)
RETURN m.name AS microbe,
       collect(DISTINCT s.id)[..5] AS example_snps,
       count(DISTINCT s) AS total_snps,
       collect(DISTINCT p.name) AS phenotypes
ORDER BY total_snps DESC;
