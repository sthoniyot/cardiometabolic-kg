// Which foods contain nutrients also produced by obesity-associated microbes?
//
MATCH (f:Food)-[:FoodToNutrient]->(n:Nutrient)
      <-[:MicrobeToNutrient]-(m:Microbe)
      -[:MicrobeToPhenotype]->(p:Phenotype {name: "obesity disorder"})
RETURN f.name AS food,
       n.name AS shared_nutrient,
       collect(DISTINCT m.name) AS obesity_microbes
LIMIT 10;
