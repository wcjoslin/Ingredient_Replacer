import json

def analyze_dietary_restrictions(enriched_ingredients, restrictions):
    """
    Analyze each enriched ingredient against user-specified dietary restrictions.
    Returns a list of flagged ingredients and rationale.
    Updated: robust category matching (case-insensitive, supports lists), and disables low-carb unless explicitly set.
    """
    # Load category mapping for robust restriction matching
    try:
        with open("data/category_mapping_and_primary_tags.json", "r", encoding="utf-8") as f:
            category_map = json.load(f)["primary_category_map"]
    except Exception:
        category_map = {}

    flagged = []
    for item in enriched_ingredients:
        ingredient = item["ingredient"]
        rationale = []
        # Use categories from enrichment (should be a list of raw keys)
        categories = item.get("categories", [])
        # Normalize categories for comparison
        categories_norm = set([c.lower().strip() for c in categories if isinstance(c, str)])

        # Map restriction category names to raw keys for robust matching
        # Synonym mapping for common diet terms
        synonym_map = {
            "dairy": ["milk", "cheese"],
            "meat": ["meat", "animal_products"],
            "nut": ["nut", "nuts"],
            "starchy vegetables": ["starchy_vegetables", "potatoes", "corn"],
            "processed foods": ["processed_foods", "packaged_foods", "ready_meals", "snacks"]
        }
        def map_restriction_categories(restriction_list):
            mapped = set()
            for r in restriction_list:
                r_norm = r.lower().replace(" ", "_").replace("-", "_").strip()
                # Expand synonyms
                expanded = [r_norm]
                if r_norm in synonym_map:
                    expanded += synonym_map[r_norm]
                for term in expanded:
                    if term in category_map:
                        mapped.update([x.lower() for x in category_map[term]])
                    elif term.rstrip("s") in category_map:
                        mapped.update([x.lower() for x in category_map[term.rstrip("s")]])
                    else:
                        mapped.add(term)
            return mapped

        # Macronutrient thresholds (generic for all rules)
        nutrition = item.get("nutrition", {})
        carbs = nutrition.get("carbohydrates", None)
        fat = nutrition.get("fat", None)
        protein = nutrition.get("protein", None)

        # Max carbohydrates
        if "max_carbohydrates_g_per_serving" in restrictions and carbs is not None:
            try:
                max_carb = float(restrictions["max_carbohydrates_g_per_serving"])
                if carbs > max_carb:
                    rationale.append(f"Carbs ({carbs}g) exceed max per serving ({max_carb}g).")
            except Exception:
                pass

        # Min fat percent
        if "min_fat_percent" in restrictions and fat is not None and nutrition.get("calories", None):
            try:
                fat_percent = (float(fat) * 9 / float(nutrition["calories"])) * 100
                min_fat = float(restrictions["min_fat_percent"])
                if fat_percent < min_fat:
                    rationale.append(f"Fat percent ({fat_percent:.1f}%) below minimum ({min_fat}%).")
            except Exception:
                pass

        # Max fat percent
        if "max_fat_percent_per_serving" in restrictions and fat is not None and nutrition.get("calories", None):
            try:
                fat_percent = (float(fat) * 9 / float(nutrition["calories"])) * 100
                max_fat = float(restrictions["max_fat_percent_per_serving"])
                if fat_percent > max_fat:
                    rationale.append(f"Fat percent ({fat_percent:.1f}%) exceeds max ({max_fat}%).")
            except Exception:
                pass

        # Category exclusion (robust, case-insensitive, mapped to raw keys)
        exclude_categories_raw = map_restriction_categories(restrictions.get("exclude_categories", []))
        # For keto, only flag if carbs > max or fat percent < min
        is_keto = "max_carbohydrates_g_per_serving" in restrictions and "min_fat_percent" in restrictions
        if exclude_categories_raw and categories_norm & exclude_categories_raw:
            if is_keto:
                # Only flag if carbs > max or fat percent < min
                flag = False
                if carbs is not None and float(carbs) > float(restrictions["max_carbohydrates_g_per_serving"]):
                    flag = True
                if fat is not None and nutrition.get("calories", None):
                    try:
                        fat_percent = (float(fat) * 9 / float(nutrition["calories"])) * 100
                        if fat_percent < float(restrictions["min_fat_percent"]):
                            flag = True
                    except Exception:
                        pass
                if flag:
                    rationale.append(f"Category {list(categories_norm & exclude_categories_raw)} is excluded by restriction.")
            else:
                rationale.append(f"Category {list(categories_norm & exclude_categories_raw)} is excluded by restriction.")

        # Ingredient exclusion (case-insensitive)
        exclude_ingredients = [e.lower().strip() for e in restrictions.get("exclude_ingredients", []) if isinstance(e, str)]
        if ingredient.lower().strip() in exclude_ingredients:
            rationale.append(f"Ingredient '{ingredient}' is excluded by restriction.")

        # Flagged allergens
        if restrictions.get("exclude_flagged_allergens") and item.get("is_flagged_allergen"):
            rationale.append(f"Ingredient '{ingredient}' is flagged as allergen.")

        # Vegan check (legacy, can be removed if category logic is robust)
        metadata = item.get("openfoodfacts_metadata", {})
        # Legacy vegan check (optional, can be removed if category logic is robust)
        exclude_categories_legacy = restrictions.get("exclude_categories", [])
        if "exclude_categories" in restrictions and "meat" in exclude_categories_legacy:
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
