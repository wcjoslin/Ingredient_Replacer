"""
ingredient_data_enrichment.py

Module for enriching recipe ingredients with nutrition and dietary category data,
and flagging dietary restrictions, using local reference files.

Checklist Steps Implemented:
- Load nutrition and category data from local files
- Load dietary restriction presets
- Normalize ingredient names for lookup
- Aggregate and format output as specified
- Enhanced: Try singular/plural forms for ingredient lookup
- Improved: Robust error handling for missing/partial data
- FIXED: Dietary restriction flagging is now case-insensitive and whitespace-normalized
"""

import json
import os

# File paths (update if needed)
NUTRITION_FILE = os.path.join("data enrichment", "enriched_ingredient_data_nutritionix.json")
CATEGORY_FILE = "foodbert_ingredient_categories_merged.json"
DIETARY_PRESETS_FILE = "dietary_restriction_presets.json"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Reference file not found: {path}")
        return None
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON in file: {path}")
        return None

def normalize_ingredient_name(name):
    import re
    return re.sub(r"[^\w\s]", "", name.lower()).strip()

def get_singular_plural_variants(name):
    from inflect import engine
    p = engine()
    norm = normalize_ingredient_name(name)
    variants = [norm]
    singular = p.singular_noun(norm)
    plural = p.plural_noun(norm)
    if singular and singular != norm:
        variants.append(singular)
    if plural and plural != norm:
        variants.append(plural)
    seen = set()
    result = []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            result.append(v)
    return result

def preprocess_nutrition_data(nutrition_list):
    nutrition_dict = {}
    if not nutrition_list:
        return nutrition_dict
    for entry in nutrition_list:
        ingr = entry.get("ingredient")
        profile = entry.get("nutritionix_nutrition_profile")
        if ingr and profile:
            norm = normalize_ingredient_name(ingr)
            nutrition_dict[norm] = profile
    return nutrition_dict

def preprocess_dietary_presets(presets_list):
    presets_dict = {}
    if not presets_list:
        return presets_dict
    for entry in presets_list:
        name = entry.get("name")
        rules = entry.get("rules")
        if name and rules:
            presets_dict[name] = rules
    return presets_dict

def get_nutrition(ingredient, nutrition_data):
    if not nutrition_data:
        return None
    for variant in get_singular_plural_variants(ingredient):
        if variant in nutrition_data:
            return nutrition_data[variant]
    return None

def get_categories(ingredient, category_data):
    if not category_data:
        return None
    for variant in get_singular_plural_variants(ingredient):
        if variant in category_data:
            return category_data[variant]
    return None

def flag_dietary_restrictions(categories, dietary_presets):
    """
    Returns a list of dietary restriction flags for the ingredient,
    based on the loaded presets and the ingredient's categories.
    Now case-insensitive and whitespace-normalized.
    """
    flags = []
    if not categories or not dietary_presets:
        return flags
    # Normalize ingredient categories for comparison
    ingredient_cats = set([c.lower().strip() for c in categories])
    for preset_name, rules in dietary_presets.items():
        exclude = set([e.lower().strip() for e in rules.get("exclude_categories", [])])
        if exclude & ingredient_cats:
            flags.append(f"Not {preset_name}")
        else:
            flags.append(f"{preset_name}-friendly")
    return flags

def enrich_ingredient(ingredient, nutrition_data, category_data, dietary_presets):
    nutrition = get_nutrition(ingredient, nutrition_data)
    categories = get_categories(ingredient, category_data)
    dietary_flags = flag_dietary_restrictions(categories, dietary_presets)

    bullet_points = []
    if nutrition:
        for key in ["calories", "protein", "carbs", "fat"]:
            if key in nutrition:
                bullet_points.append(f"{key.capitalize()}: {nutrition[key]}")
            elif key == "carbs" and "carbohydrates" in nutrition:
                bullet_points.append(f"Carbs: {nutrition['carbohydrates']}")
    if categories:
        bullet_points.extend([f"Category: {cat}" for cat in categories])
    if dietary_flags:
        bullet_points.extend(dietary_flags)
    if not nutrition and not categories:
        bullet_points.append(
            f"Nutritional Information for {ingredient} is incomplete at this time, unable to find dietary information at this time"
        )
    elif not nutrition:
        bullet_points.append(
            f"Nutritional Information for {ingredient} is incomplete at this time"
        )
    elif not categories:
        bullet_points.append(
            f"Dietary category information for {ingredient} is incomplete at this time"
        )
    return bullet_points

def enrich_recipe_ingredients(ingredient_list):
    nutrition_list = load_json(NUTRITION_FILE)
    nutrition_data = preprocess_nutrition_data(nutrition_list)
    category_data = load_json(CATEGORY_FILE)
    dietary_presets_list = load_json(DIETARY_PRESETS_FILE)
    dietary_presets = preprocess_dietary_presets(dietary_presets_list)

    enriched = {}
    for ingredient in ingredient_list:
        enriched[ingredient] = enrich_ingredient(
            ingredient, nutrition_data, category_data, dietary_presets
        )
    return enriched

if __name__ == "__main__":
    test_ingredients = ["Egg", "Milk", "Flour", "Unknown Ingredient"]
    enriched = enrich_recipe_ingredients(test_ingredients)
    for ingr, bullets in enriched.items():
        print(f"{ingr}:")
        for b in bullets:
            print(f"  - {b}")
        print()
