// Which gut microbes are directly associated with type 2 diabetes?
//
MATCH (m:Microbe)-[r:MicrobeToPhenotype]->(p:Phenotype {name: "type 2 diabetes mellitus"})
RETURN m.name AS microbe,
       m.rank AS rank,
       r.evidence_tier AS evidence;
