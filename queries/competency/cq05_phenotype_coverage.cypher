// How many SNPs are associated with each cardiometabolic phenotype?
//
MATCH (s:Snp)-[:SnpToPhenotype]->(p:Phenotype)
RETURN p.name AS phenotype,
       count(DISTINCT s) AS n_snps
ORDER BY n_snps DESC;
