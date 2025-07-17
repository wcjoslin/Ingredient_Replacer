import json
from integrate_usda_openfoodfacts import enrich_ingredient_data
from dietary_restriction_analysis import analyze_dietary_restrictions
from ingredient_swap_suggestions import suggest_swaps

def run_ingredient_workflow(recipe_path, restrictions, output_prefix="final_recipe_swap"):
    """
    Orchestrates the full ingredient substitution workflow.
    1. Loads a recipe.
    2. Enriches its ingredients with nutritional and metadata.
    3. Flags ingredients based on dietary restrictions.
    4. Finds the best swap for each flagged ingredient using the enhanced scoring model.
    """
    # Step 1: Load recipe
    with open(recipe_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)
    
    # Assuming the recipe JSON has a list of ingredients under a key like "ingredients"
    # This part might need adjustment based on the actual recipe format.
    # For this example, we'll stick to the format from `diet_test_recipe_details.json`
    ingredients = [i["name"] for i in recipe["pre_diabetic"]["ingredients"]]

    # Step 2: Enrich ingredient data
    enriched_data = enrich_ingredient_data(ingredients)
    
    # Step 3: Flag ingredients based on restrictions
    flagged_ingredients = analyze_dietary_restrictions(enriched_data, restrictions)

    # Early filtering: Remove spices and ingredients already meeting nutrition/category rules
    from ingredient_swap_suggestions import COMMON_SPICES
    filtered_flagged = []
    for item in flagged_ingredients:
        name = item["ingredient"].lower().strip()
        # Skip common spices
        if name in COMMON_SPICES:
            continue
        # Skip ingredients already meeting low-carb rule (<=10g carbs)
        nutrition = item.get("nutrition", {})
        if nutrition and nutrition.get("carbohydrates", 0) <= 10:
            continue
        # TODO: Add category filtering if needed
        filtered_flagged.append(item)

    flagged_path = f"{output_prefix}_flagged_ingredients.json"
    with open(flagged_path, "w", encoding="utf-8") as f:
        json.dump(filtered_flagged, f, ensure_ascii=False, indent=2)

    # Step 4: Get swap suggestions for flagged ingredients
    suggest_swaps(flagged_path, output_path_prefix=f"{output_prefix}_suggestions")

    print(f"Workflow complete. Flagged ingredients saved to {flagged_path}.")
    print(f"Swap suggestions saved to {output_prefix}_suggestions.json")

if __name__ == "__main__":
    # Define the dietary restrictions for the run
    # In this case, we want to flag ingredients that are high in carbs.
    restrictions = {
        "low-carb": 40,  # Flag any ingredient with more than 40g of carbs
    }
    
    # Specify the recipe to process
    recipe_file = "diet_test_recipe_details.json"
    
    # Run the full workflow
    run_ingredient_workflow(recipe_file, restrictions)
