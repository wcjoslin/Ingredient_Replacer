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

        # Example restriction checks
        if "low-carb" in restrictions and usda_carbs is not None and usda_carbs > restrictions["low-carb"]:
            rationale.append(f"Carbs ({usda_carbs}g) exceed low-carb threshold ({restrictions['low-carb']}g).")
        if "vegan" in restrictions and metadata:
            if not any("vegan" in tag for tag in metadata.get("vegan", [])):
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
