import json

def analyze_dietary_restrictions(enriched_ingredients, restrictions):
    """
    Analyze each enriched ingredient against user-specified dietary restrictions.
    Returns a list of flagged ingredients and rationale.
    Updated: robust category matching (case-insensitive, supports lists), and disables low-carb unless explicitly set.
    """
    flagged = []
    for item in enriched_ingredients:
        ingredient = item["ingredient"]
        rationale = []
        # Use categories from enrichment (should be a list of raw keys)
        categories = item.get("categories", [])
        # Normalize categories for comparison
        categories_norm = set([c.lower().strip() for c in categories if isinstance(c, str)])

        # Macronutrient threshold (only if explicitly set)
        nutrition = item.get("nutrition", {})
        carbs = nutrition.get("carbohydrates", None)
        if "max_carbohydrates_g_per_serving" in restrictions and carbs is not None:
            try:
                max_carb = float(restrictions["max_carbohydrates_g_per_serving"])
                if carbs > max_carb:
                    rationale.append(f"Carbs ({carbs}g) exceed max per serving ({max_carb}g).")
            except Exception:
                pass

        # Category exclusion (robust, case-insensitive)
        exclude_categories = set([e.lower().strip() for e in restrictions.get("exclude_categories", []) if isinstance(e, str)])
        if exclude_categories and categories_norm & exclude_categories:
            rationale.append(f"Category {list(categories_norm & exclude_categories)} is excluded by restriction.")

        # Ingredient exclusion (case-insensitive)
        exclude_ingredients = [e.lower().strip() for e in restrictions.get("exclude_ingredients", []) if isinstance(e, str)]
        if ingredient.lower().strip() in exclude_ingredients:
            rationale.append(f"Ingredient '{ingredient}' is excluded by restriction.")

        # Flagged allergens
        if restrictions.get("exclude_flagged_allergens") and item.get("is_flagged_allergen"):
            rationale.append(f"Ingredient '{ingredient}' is flagged as allergen.")

        # Vegan check (legacy, can be removed if category logic is robust)
        metadata = item.get("openfoodfacts_metadata", {})
        if "exclude_categories" in restrictions and "meat" in exclude_categories:
            if metadata and not any("vegan" in tag for tag in metadata.get("vegan", [])):
                rationale.append("Ingredient may not be vegan.")

        # Add more checks as needed

        if rationale:
            flagged.append({
                "ingredient": ingredient,
                "rationale": rationale,
                "nutrition": nutrition,
                "categories": list(categories_norm),
                "metadata": metadata
            })
    return flagged

if __name__ == "__main__":
    # Example: Load enriched ingredient data
    with open("data/enriched_ingredient_data.json", "r", encoding="utf-8") as f:
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
