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

    # Step 2: Enrich ingredient data using Nutritionix reference
    with open("data enrichment/enriched_ingredient_data_nutritionix.json", "r", encoding="utf-8") as nut_file:
        nutritionix_list = json.load(nut_file)
    nutritionix_data = {entry["ingredient"].lower().strip(): entry["nutritionix_nutrition_profile"] for entry in nutritionix_list}
    enriched_data = []
    for ingredient in ingredients:
        nutrition = nutritionix_data.get(ingredient.lower().strip(), {})
        enriched_data.append({"ingredient": ingredient, "nutrition": nutrition})
    
    # Step 3: Flag ingredients based on restrictions
    flagged_ingredients = analyze_dietary_restrictions(enriched_data, restrictions)

    # Early filtering: Remove spices, ingredients already meeting nutrition/category rules, and mismatched categories
    from ingredient_swap_suggestions import COMMON_SPICES
    with open("ingredient_primary_categories.json", "r", encoding="utf-8") as cat_file:
        primary_categories = json.load(cat_file)
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
        # Category filtering: Only allow replacements with matching primary category
        target_category = primary_categories.get(name)
        if not target_category:
            continue
        # Only keep if candidate's category matches the flagged ingredient's category
        if primary_categories.get(name) != target_category:
            continue
        filtered_flagged.append(item)

    flagged_path = f"{output_prefix}_flagged_ingredients.json"
    with open(flagged_path, "w", encoding="utf-8") as f:
        json.dump(filtered_flagged, f, ensure_ascii=False, indent=2)

    # Step 4: Get swap suggestions for flagged ingredients
    suggest_swaps(flagged_path, output_path_prefix=f"{output_prefix}_suggestions", restrictions=restrictions)

    # (DEBUG OUTPUT REMOVED)

if __name__ == "__main__":
    import json
    import argparse

    parser = argparse.ArgumentParser(description="Run ingredient workflow with selected dietary restrictions.")
    parser.add_argument("--restriction_ids", type=str, default="", help="Comma-separated list of restriction IDs (e.g., low_carb,vegan)")
    parser.add_argument("--recipe_file", type=str, default="diet_test_recipe_details.json", help="Recipe file to process")
    args = parser.parse_args()

    # Parse restriction IDs
    restriction_ids = [rid.strip() for rid in args.restriction_ids.split(",") if rid.strip()]
    if not restriction_ids:
        print("No restriction_ids specified. Please provide at least one restriction ID using --restriction_ids.")
        exit(1)

    # Load presets
    with open("dietary_restriction_presets.json", "r", encoding="utf-8") as f:
        presets = json.load(f)

    # Merge rules from selected presets
    merged_rules = {}
    for rid in restriction_ids:
        preset = next((p for p in presets if p["id"] == rid), None)
        if preset:
            for k, v in preset["rules"].items():
                # For numeric rules, use the strictest value (lowest for max, highest for min)
                if k.startswith("max_"):
                    if k not in merged_rules or v < merged_rules[k]:
                        merged_rules[k] = v
                elif k.startswith("min_"):
                    if k not in merged_rules or v > merged_rules[k]:
                        merged_rules[k] = v
                elif isinstance(v, list):
                    merged_rules.setdefault(k, []).extend([item for item in v if item not in merged_rules.get(k, [])])
                else:
                    merged_rules[k] = v

    run_ingredient_workflow(args.recipe_file, merged_rules)
