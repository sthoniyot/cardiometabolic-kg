// Which foods have the highest total dietary fiber content?
//
MATCH (f:Food)-[r:FoodToNutrient]->(n:Nutrient {name: "Fiber, total dietary"})
RETURN f.name AS food,
       r.concentration AS fiber_g_per_100g,
       r.unit AS unit
ORDER BY r.concentration DESC
LIMIT 10;
