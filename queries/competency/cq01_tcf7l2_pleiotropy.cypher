// Which cardiometabolic SNPs map to TCF7L2 and their effect sizes?
//
MATCH (s:Snp)-[:SnpToGene]->(g:Gene {symbol: "TCF7L2"})
MATCH (s)-[r:SnpToPhenotype]->(p:Phenotype)
RETURN s.id AS snp,
       p.name AS disease,
       r.effect_size AS effect_size,
       r.p_value AS p_value,
       r.pmid AS pmid
ORDER BY r.p_value
LIMIT 10;
