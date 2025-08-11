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
CATEGORY_FILE = os.path.join("src","foodbert_ingredient_categories_merged.json")
DIETARY_PRESETS_FILE = "data/dietary_restriction_presets.json"

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
        # Use "id" as key for correct mapping to selected diets
        key = entry.get("id") or entry.get("name")
        rules = entry.get("rules")
        if key and rules:
            presets_dict[key] = rules
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
    # Normalize ingredient categories for comparison, strip "en:" prefix
    def norm(cat):
        c = cat.lower().strip()
        return c[3:] if c.startswith("en:") else c
    ingredient_cats = set([norm(c) for c in categories])
    for preset_name, rules in dietary_presets.items():
        exclude = set([norm(e) for e in rules.get("exclude_categories", [])])
        if exclude & ingredient_cats:
            flags.append(f"Not {preset_name}")
        else:
            flags.append(f"{preset_name}-friendly")
    return flags

def enrich_ingredient(ingredient, nutrition_data, category_data, dietary_presets):
    nutrition = get_nutrition(ingredient, nutrition_data)
    categories = get_categories(ingredient, category_data)
    dietary_flags = flag_dietary_restrictions(categories, dietary_presets)

    # Nutrition facts as dict
    nutrition_facts = {}
    if nutrition:
        for key in ["calories", "protein", "carbs", "fat"]:
            if key in nutrition:
                nutrition_facts[key] = nutrition[key]
            elif key == "carbs" and "carbohydrates" in nutrition:
                nutrition_facts["carbs"] = nutrition["carbohydrates"]

    # Categories as list
    categories_list = categories if categories else []

    # Swap rationales: reasons for being flagged (nutrition/category)
    swap_rationales = []
    if dietary_flags:
        for flag in dietary_flags:
            if flag.startswith("Not "):
                # Example: "Not Vegan" or "Not Keto"
                reason = flag.replace("Not ", "")
                if categories_list:
                    swap_rationales.append(f"Category: {reason} excluded")
                else:
                    swap_rationales.append(f"Category restriction: {reason}")
            # else: "{diet}-friendly" (not flagged)

    # Description of dietary change (if flagged)
    dietary_change_description = ""
    if swap_rationales:
        dietary_change_description = "Ingredient does not comply with selected diet(s): " + "; ".join(swap_rationales)

    # Bullet points for display
    bullet_points = []
    if nutrition_facts:
        for k, v in nutrition_facts.items():
            bullet_points.append(f"{k.capitalize()}: {v}")
    if categories_list:
        bullet_points.extend([f"Category: {cat}" for cat in categories_list])
    if swap_rationales:
        bullet_points.extend([f"Flagged: {r}" for r in swap_rationales])
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

    return {
        "ingredient": ingredient,
        "nutrition_facts": nutrition_facts,
        "categories": categories_list,
        "swap_rationales": swap_rationales,
        "dietary_change_description": dietary_change_description,
        "bullet_points": bullet_points
    }

from src.ingredient_workflow import normalize_ingredient_string, extract_core_ingredient_spacy

def enrich_recipe_ingredients(ingredient_list):
    nutrition_list = load_json(NUTRITION_FILE)
    nutrition_data = preprocess_nutrition_data(nutrition_list)
    category_data = load_json(CATEGORY_FILE)
    dietary_presets_list = load_json(DIETARY_PRESETS_FILE)
    dietary_presets = preprocess_dietary_presets(dietary_presets_list)

    enriched = []
    for ingredient in ingredient_list:
        # Apply spaCy-based normalization before enrichment
        norm_ingr = normalize_ingredient_string(ingredient)
        core_ingr = extract_core_ingredient_spacy(norm_ingr)
        enriched.append(
            enrich_ingredient(
                core_ingr, nutrition_data, category_data, dietary_presets
            )
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
