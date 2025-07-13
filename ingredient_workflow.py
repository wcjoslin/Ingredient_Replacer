import json
from integrate_usda_openfoodfacts import enrich_ingredient_data
from dietary_restriction_analysis import analyze_dietary_restrictions

def run_ingredient_workflow(recipe_details_path, restrictions, output_prefix="workflow"):
    # Step 1: Load recipe details
    with open(recipe_details_path, "r", encoding="utf-8") as f:
        recipe_details = json.load(f)
    # Example: Use pre_diabetic test
    ingredients = [i["name"] for i in recipe_details["pre_diabetic"]["ingredients"]]
    
    # Step 2: Enrich ingredient data
    enriched_data = enrich_ingredient_data(ingredients)
    enriched_path = f"{output_prefix}_enriched_ingredient_data.json"
    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    
    # Step 3: Analyze dietary restrictions
    flagged = analyze_dietary_restrictions(enriched_data, restrictions)
    flagged_path = f"{output_prefix}_flagged_ingredients.json"
    with open(flagged_path, "w", encoding="utf-8") as f:
        json.dump(flagged, f, ensure_ascii=False, indent=2)
    
    print(f"Workflow complete. Enriched data saved to {enriched_path}, flagged ingredients saved to {flagged_path}.")

if __name__ == "__main__":
    restrictions = {
        "low-carb": 5,  # grams per ingredient
        "vegan": True,
        "kosher": True,
        "halal": False
    }
    run_ingredient_workflow("diet_test_recipe_details.json", restrictions)
