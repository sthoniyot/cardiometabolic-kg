// Which metabolites are produced by both foods and gut microbes?
//
MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)
      <-[:MicrobeToNutrient]-(m:Microbe)
RETURN n.name AS shared_metabolite,
       count(DISTINCT f) AS n_foods,
       count(DISTINCT m) AS n_microbes,
       collect(DISTINCT f.name)[..3] AS example_foods,
       collect(DISTINCT m.name)[..3] AS example_microbes
ORDER BY n_foods DESC;
