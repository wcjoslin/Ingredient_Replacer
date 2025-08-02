import json
from openfoodfacts_api import get_product_metadata

# Load the Nutritionix enrichment library once at module load
with open("data enrichment/enriched_ingredient_data_nutritionix.json", "r", encoding="utf-8") as f:
    NUTRITIONIX_LIBRARY = {entry["ingredient"].lower().strip(): entry["nutritionix_nutrition_profile"] for entry in json.load(f)}

def enrich_ingredient_data(ingredient_list):
    enriched = []
    for ingredient in ingredient_list:
        normalized = ingredient.lower().strip()
        # Use the saved Nutritionix data instead of calling the API
        nutritionix_profile = NUTRITIONIX_LIBRARY.get(normalized)
        # Special handling for black pepper (if not present)
        if normalized in ["black pepper", "pepper", "black peppercorns"] and not nutritionix_profile:
            nutritionix_profile = {
                "calories": 5.8,
                "protein": 0.2,
                "fat": 0.1,
                "carbohydrates": 1.5
            }
            off_metadata = {
                "vegan": ["en:vegan", "en:vegetarian"],
                "allergens": [],
                "labels": [],
                "categories": ["en:spices", "en:black-pepper"]
            }
        else:
            off_metadata = get_product_metadata(ingredient)
        enriched.append({
            "ingredient": ingredient,
            "nutritionix_nutrition_profile": nutritionix_profile,
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
with open("data/enriched_ingredient_data.json", "w", encoding="utf-8") as f:
    json.dump(enriched_data, f, ensure_ascii=False, indent=2)
