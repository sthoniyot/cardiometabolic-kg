// Which gut microbes are known to produce butyrate or other short-chain fatty acids?
//
MATCH (m:Microbe)-[:MicrobeToNutrient]->(n:Nutrient)
WHERE toLower(n.name) CONTAINS "butyr"
   OR toLower(n.name) CONTAINS "propion"
   OR toLower(n.name) CONTAINS "acetate"
RETURN m.name AS microbe,
       n.name AS metabolite,
       n.id AS chebi
LIMIT 20;
