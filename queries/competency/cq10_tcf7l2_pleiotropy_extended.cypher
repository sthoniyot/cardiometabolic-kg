// How many distinct cardiometabolic phenotypes does each TCF7L2 SNP touch?
//
MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})
MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)
RETURN s.id AS snp,
       count(DISTINCT p) AS n_phenotypes,
       collect(DISTINCT p.name) AS phenotypes
ORDER BY n_phenotypes DESC
LIMIT 10;
