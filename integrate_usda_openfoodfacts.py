import json
from usda_api import get_food_carbs
from openfoodfacts_api import get_product_metadata

def enrich_ingredient_data(ingredient_list):
    enriched = []
    for ingredient in ingredient_list:
        usda_carbs = get_food_carbs(ingredient)
        off_metadata = get_product_metadata(ingredient)
        enriched.append({
            "ingredient": ingredient,
            "usda_carbs": usda_carbs,
            "openfoodfacts_metadata": off_metadata
        })
    return enriched

if __name__ == "__main__":
    # Example: Load ingredients from a test file
    with open("diet_test_recipe_details.json", "r", encoding="utf-8") as f:
        recipe_details = json.load(f)
    # Use pre_diabetic test as example
    ingredients = [i["name"] for i in recipe_details["pre_diabetic"]["ingredients"]]
    enriched_data = enrich_ingredient_data(ingredients)
    with open("enriched_ingredient_data.json", "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
