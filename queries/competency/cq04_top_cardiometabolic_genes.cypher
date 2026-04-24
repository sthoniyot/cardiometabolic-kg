// Which genes carry the most cardiometabolic GWAS signals?
//
MATCH (s:Snp)-[:SnpToGene]->(g:Gene)
RETURN g.symbol AS gene,
       count(DISTINCT s) AS n_snps
ORDER BY n_snps DESC
LIMIT 15;
