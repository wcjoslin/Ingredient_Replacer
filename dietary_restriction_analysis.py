import json

def analyze_dietary_restrictions(enriched_ingredients, restrictions):
    """
    Analyze each enriched ingredient against user-specified dietary restrictions.
    Returns a list of flagged ingredients and rationale.
    """
    flagged = []
    for item in enriched_ingredients:
        ingredient = item["ingredient"]
        # Extract carbs from usda_nutrition_profile if present
        usda_nutrition = item.get("usda_nutrition_profile", {})
        usda_carbs = None
        if isinstance(usda_nutrition, dict):
            usda_carbs = usda_nutrition.get("carbohydrates")
        metadata = item.get("openfoodfacts_metadata", {})
        rationale = []

        # Apply merged dietary restriction rules
        # Macronutrient threshold
        from ingredient_swap_suggestions import get_nutrition_profile
        nutrition = get_nutrition_profile(ingredient)
        carbs = nutrition.get("carbohydrates", None)
        if "max_carbohydrates_g_per_serving" in restrictions and carbs is not None:
            if carbs > restrictions["max_carbohydrates_g_per_serving"]:
                rationale.append(f"Carbs ({carbs}g) exceed max per serving ({restrictions['max_carbohydrates_g_per_serving']}g).")
        if "max_fat_percent_per_serving" in restrictions and nutrition.get("fat_percent") is not None:
            if nutrition["fat_percent"] > restrictions["max_fat_percent_per_serving"]:
                rationale.append(f"Fat percent ({nutrition['fat_percent']}%) exceeds max per serving ({restrictions['max_fat_percent_per_serving']}%).")
        # Category exclusion
        if "exclude_categories" in restrictions and item.get("primary_category") in restrictions["exclude_categories"]:
            rationale.append(f"Category '{item.get('primary_category')}' is excluded by restriction.")
        # Ingredient exclusion
        if "exclude_ingredients" in restrictions and ingredient.lower() in [e.lower() for e in restrictions["exclude_ingredients"]]:
            rationale.append(f"Ingredient '{ingredient}' is excluded by restriction.")
        # Flagged allergens
        if restrictions.get("exclude_flagged_allergens") and item.get("is_flagged_allergen"):
            rationale.append(f"Ingredient '{ingredient}' is flagged as allergen.")
        # Vegan check
        if "exclude_categories" in restrictions and "meat" in restrictions["exclude_categories"]:
            if metadata and not any("vegan" in tag for tag in metadata.get("vegan", [])):
                rationale.append("Ingredient may not be vegan.")
        # Add more checks as needed

        if rationale:
            flagged.append({
                "ingredient": ingredient,
                "rationale": rationale,
                "usda_carbs": usda_carbs,
                "metadata": metadata
            })
    return flagged

if __name__ == "__main__":
    # Example: Load enriched ingredient data
    with open("enriched_ingredient_data.json", "r", encoding="utf-8") as f:
        enriched_ingredients = json.load(f)
    # Example restrictions
    restrictions = {
        "low-carb": 5,  # grams per ingredient
        "vegan": True,
        "kosher": True,
        "halal": False
    }
    flagged = analyze_dietary_restrictions(enriched_ingredients, restrictions)
    with open("flagged_ingredients.json", "w", encoding="utf-8") as f:
        json.dump(flagged, f, ensure_ascii=False, indent=2)
