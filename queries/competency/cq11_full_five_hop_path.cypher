// Is there a full Food -> Nutrient <- Microbe -> Gene <- SNP -> Phenotype path? (tri-layer)
//
MATCH path = (f:Food)-[:FoodToNutrient]->(n:Nutrient)
             <-[:MicrobeToNutrient]-(m:Microbe)
             -[:MicrobeToGene]->(g:Gene)
             <-[:SnpToGene]-(s:Snp)
             -[:SnpToPhenotype]->(p:Phenotype)
RETURN f.name AS food,
       n.name AS nutrient,
       m.name AS microbe,
       g.symbol AS gene,
       s.id AS snp,
       p.name AS phenotype
LIMIT 10;
