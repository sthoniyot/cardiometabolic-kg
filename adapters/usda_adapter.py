"""
USDA FoodData Central adapter for cardiometabolic KG.

Reads the Foundation Foods CSV release and yields:
  - Food nodes (filtered to foundation_food only, ~200 high-quality foods)
  - Nutrient nodes (with hand-curated CHEBI mapping for key cardiometabolic nutrients)
  - Food->Nutrient edges with concentration and unit
"""
import csv
import os

USDA_DIR = "data/raw/usda/FoodData_Central_foundation_food_csv_2024-04-18"

# Hand-curated CHEBI mapping for the most biologically important nutrients.
# USDA nutrient_nbr (from nutrient.csv) -> (CHEBI ID, compound_class).
# Where no exact CHEBI equivalent exists or we want to keep USDA provenance,
# the nutrient falls through to the USDA:<id> fallback.
NUTRIENT_NBR_TO_CHEBI = {
    "203": ("CHEBI:36080", "protein"),             # Protein
    "204": ("CHEBI:17855", "lipid"),                # Total lipid (fat)
    "205": ("CHEBI:16646", "carbohydrate"),         # Carbohydrate, by difference
    "207": ("CHEBI:33252", "ash"),                  # Ash
    "208": ("CHEBI:30431", "energy"),               # Energy (kcal) - not a compound, skip in graph
    "269": ("CHEBI:17234", "carbohydrate"),         # Total Sugars
    "291": ("CHEBI:33290", "fiber"),                # Fiber, total dietary
    "295": ("CHEBI:33290", "fiber"),                # Fiber, soluble
    "297": ("CHEBI:33290", "fiber"),                # Fiber, insoluble
    "301": ("CHEBI:22984", "mineral"),              # Calcium
    "303": ("CHEBI:24875", "mineral"),              # Iron
    "304": ("CHEBI:25107", "mineral"),              # Magnesium
    "305": ("CHEBI:28659", "mineral"),              # Phosphorus
    "306": ("CHEBI:26216", "mineral"),              # Potassium
    "307": ("CHEBI:26708", "mineral"),              # Sodium
    "309": ("CHEBI:27363", "mineral"),              # Zinc
    "312": ("CHEBI:28694", "mineral"),              # Copper
    "315": ("CHEBI:18291", "mineral"),              # Manganese
    "317": ("CHEBI:27568", "mineral"),              # Selenium
    "318": ("CHEBI:22915", "vitamin"),              # Vitamin A, IU
    "323": ("CHEBI:33234", "vitamin"),              # Vitamin E (alpha-tocopherol)
    "328": ("CHEBI:27300", "vitamin"),              # Vitamin D
    "401": ("CHEBI:29073", "vitamin"),              # Vitamin C (ascorbic acid)
    "404": ("CHEBI:26948", "vitamin"),              # Thiamin (B1)
    "405": ("CHEBI:17015", "vitamin"),              # Riboflavin (B2)
    "406": ("CHEBI:17154", "vitamin"),              # Niacin (B3)
    "410": ("CHEBI:44258", "vitamin"),              # Pantothenic acid (B5)
    "415": ("CHEBI:27306", "vitamin"),              # Vitamin B-6
    "417": ("CHEBI:16796", "vitamin"),              # Folate, total
    "418": ("CHEBI:17439", "vitamin"),              # Vitamin B-12
    "430": ("CHEBI:28384", "vitamin"),              # Vitamin K
    "601": ("CHEBI:16113", "lipid"),                # Cholesterol
    "606": ("CHEBI:26607", "lipid"),                # Fatty acids, saturated
    "645": ("CHEBI:59548", "lipid"),                # Fatty acids, monounsaturated
    "646": ("CHEBI:26208", "lipid"),                # Fatty acids, polyunsaturated
    "851": ("CHEBI:50382", "omega_3"),              # ALA (18:3 n-3)
    "858": ("CHEBI:28364", "omega_3"),              # EPA (20:5 n-3)
    "875": ("CHEBI:28125", "omega_3"),              # DHA (22:6 n-3)
    "950": ("CHEBI:22868", "sterol"),               # Phytosterols
}

# Nutrients we want to skip even if they appear (not biologically meaningful for the KG)
SKIP_NUTRIENTS = {
    "208",  # Energy (kcal) - not a molecular entity
    "957",  # Energy (Atwater General Factors)
    "958",  # Energy (Atwater Specific Factors)
    "268",  # Energy (kJ)
}


class USDAAdapter:
    def __init__(self, usda_dir=USDA_DIR):
        self.usda_dir = usda_dir
        self._foods = {}           # fdc_id -> props
        self._nutrients = {}       # nutrient_id -> (chebi_id_or_usda, props)
        self._food_nutrient_edges = []
        self._categories = {}      # category_id -> description
        self._nutrient_meta = {}   # nutrient_id -> {name, unit, nbr}
        self._nutrient_id_map = {} # nutrient_id -> chebi or USDA fallback ID
        self._parse()

    def _read_csv(self, filename):
        path = os.path.join(self.usda_dir, filename)
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _parse(self):
        # 1. Categories
        for row in self._read_csv("food_category.csv"):
            self._categories[row["id"]] = row["description"]

        # 2. Nutrients
        for row in self._read_csv("nutrient.csv"):
            nid = row["id"]
            nbr = row["nutrient_nbr"]
            if nbr in SKIP_NUTRIENTS:
                continue
            self._nutrient_meta[nid] = {
                "name": row["name"],
                "unit": row["unit_name"],
                "nbr": nbr,
            }
            # Resolve to CHEBI or fallback
            if nbr in NUTRIENT_NBR_TO_CHEBI:
                chebi_id, compound_class = NUTRIENT_NBR_TO_CHEBI[nbr]
                self._nutrient_id_map[nid] = chebi_id
                if chebi_id not in self._nutrients:
                    self._nutrients[chebi_id] = {
                        "name": row["name"],
                        "compound_class": compound_class,
                    }
            else:
                fallback_id = f"USDA:{nbr}"
                self._nutrient_id_map[nid] = fallback_id
                if fallback_id not in self._nutrients:
                    self._nutrients[fallback_id] = {
                        "name": row["name"],
                        "compound_class": "other",
                    }

        # 3. Foods (only foundation_food)
        for row in self._read_csv("food.csv"):
            if row["data_type"] != "foundation_food":
                continue
            fdc_id = row["fdc_id"]
            cat_id = row.get("food_category_id", "").strip()
            food_group = self._categories.get(cat_id, "")
            food_node_id = f"FDC:{fdc_id}"
            self._foods[food_node_id] = {
                "name": row["description"],
                "food_group": food_group,
            }

        # 4. Food -> Nutrient edges
        allowed_food_ids = set(self._foods.keys())
        for row in self._read_csv("food_nutrient.csv"):
            fdc_id = row["fdc_id"]
            food_node_id = f"FDC:{fdc_id}"
            if food_node_id not in allowed_food_ids:
                continue
            nid = row["nutrient_id"]
            if nid not in self._nutrient_id_map:
                continue
            amount_str = row.get("amount", "").strip()
            if not amount_str:
                continue
            try:
                amount = float(amount_str)
            except ValueError:
                continue
            if amount <= 0:
                continue
            meta = self._nutrient_meta[nid]
            nutrient_node_id = self._nutrient_id_map[nid]
            self._food_nutrient_edges.append((
                food_node_id,
                nutrient_node_id,
                {
                    "concentration": amount,
                    "unit": meta["unit"],
                },
            ))

    def get_nodes(self):
        for food_id, props in self._foods.items():
            yield (food_id, "food", props)
        for nutrient_id, props in self._nutrients.items():
            yield (nutrient_id, "nutrient", props)

    def get_edges(self):
        for i, (src, tgt, props) in enumerate(self._food_nutrient_edges):
            yield (f"fn_{i}", src, tgt, "food_to_nutrient", props)

    def stats(self):
        return {
            "foods": len(self._foods),
            "nutrients": len(self._nutrients),
            "food_nutrient_edges": len(self._food_nutrient_edges),
        }
