import json
import pickle
import numpy as np
import re
import sys
from sklearn.preprocessing import StandardScaler

from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier
from nutritional_analysis import calculate_nutrition_delta
from culinary_rules import is_culinarily_valid
from usda_api import get_food_nutrition_profile

# List of common spices to exclude from low-carb swaps and update nutrition for
COMMON_SPICES = {
    "black pepper", "cumin", "paprika", "chili powder", "garlic powder", "onion powder",
    "cinnamon", "nutmeg", "cloves", "coriander", "thyme", "basil", "oregano"
}

# Nutritionix reference values for spices (per 1 tsp, ground)
SPICE_NUTRITION = {
    "black pepper": {"calories": 6, "protein": 0.0, "fat": 0.0, "carbohydrates": 0.9},
    "cumin": {"calories": 8, "protein": 0.4, "fat": 0.5, "carbohydrates": 0.7},
    "paprika": {"calories": 6, "protein": 0.3, "fat": 0.3, "carbohydrates": 0.6},
    "chili powder": {"calories": 8, "protein": 0.4, "fat": 0.4, "carbohydrates": 0.7},
    "garlic powder": {"calories": 10, "protein": 0.5, "fat": 0.0, "carbohydrates": 2.2},
    "onion powder": {"calories": 8, "protein": 0.2, "fat": 0.0, "carbohydrates": 1.6},
    "cinnamon": {"calories": 6, "protein": 0.1, "fat": 0.0, "carbohydrates": 0.7},
    "nutmeg": {"calories": 12, "protein": 0.1, "fat": 0.8, "carbohydrates": 0.6},
    "cloves": {"calories": 6, "protein": 0.1, "fat": 0.3, "carbohydrates": 0.7},
    "coriander": {"calories": 5, "protein": 0.2, "fat": 0.1, "carbohydrates": 0.3},
    "thyme": {"calories": 3, "protein": 0.1, "fat": 0.1, "carbohydrates": 0.2},
    "basil": {"calories": 1, "protein": 0.1, "fat": 0.0, "carbohydrates": 0.1},
    "oregano": {"calories": 3, "protein": 0.1, "fat": 0.1, "carbohydrates": 0.3},
    "garlic": {"calories": 10, "protein": 0.5, "fat": 0.0, "carbohydrates": 2.2}  # Added garlic as per Nutritionix
}

# Load master ingredient categories for filtering
with open("foodbert_ingredient_categories_merged.json", "r", encoding="utf-8") as f:
    INGREDIENT_CATEGORIES = json.load(f)
with open("ingredient_primary_categories.json", "r", encoding="utf-8") as f:
    INGREDIENT_PRIMARY_CATEGORIES = json.load(f)
with open("data/category_mapping_and_primary_tags.json", "r", encoding="utf-8") as f:
    CATEGORY_MAPPING = json.load(f)

def normalize_ingredient_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)
    return name

def aggregate_embeddings_max(emb_matrix):
    return np.max(emb_matrix, axis=0)

def get_allowed_categories(primary, dietary_goal=None):
    # Default allowed swaps
    allowed = set(CATEGORY_MAPPING["default_allowed_swaps"].get(primary, []))
    # Special diet overrides
    if dietary_goal:
        special = CATEGORY_MAPPING["special_diet_swaps"].get(dietary_goal, {})
        allowed.update(special.get(primary, []))
    return allowed

# Nutrition profile cache
NUTRITION_CACHE = {}

def get_nutrition_profile(ingredient):
    norm_ingredient = normalize_ingredient_name(ingredient)
    # Always use Nutritionix reference for common spices and garlic
    if norm_ingredient in SPICE_NUTRITION:
        return SPICE_NUTRITION[norm_ingredient]
    # Load Nutritionix reference data for all ingredients
    try:
        with open("data enrichment/enriched_ingredient_data_nutritionix.json", "r", encoding="utf-8") as nut_file:
            nutritionix_list = json.load(nut_file)
        nutritionix_data = {entry["ingredient"].lower().strip(): entry["nutritionix_nutrition_profile"] for entry in nutritionix_list}
        if norm_ingredient in nutritionix_data:
            return nutritionix_data[norm_ingredient]
    except Exception as e:
        pass
    # Use cache if available
    if norm_ingredient in NUTRITION_CACHE:
        return NUTRITION_CACHE[norm_ingredient]
    # Otherwise use main lookup
    profile = get_food_nutrition_profile(norm_ingredient)
    NUTRITION_CACHE[norm_ingredient] = profile
    return profile

def get_enhanced_swap(ingredient, embedding_dict, knn, ingredient_labels, scaler=None, restrictions=None):
    norm_ingredient = normalize_ingredient_name(ingredient)
    print(f"DEBUG: Processing ingredient '{ingredient}' (normalized: '{norm_ingredient}')")
    if norm_ingredient not in embedding_dict:
        print(f"DEBUG: Ingredient '{norm_ingredient}' not found in embedding dictionary.")
        return {"error": f"Ingredient '{ingredient}' (normalized: '{norm_ingredient}') not in embedding vocabulary."}

    original_nutrition = get_nutrition_profile(norm_ingredient)
    print(f"DEBUG: Original nutrition for '{norm_ingredient}': {original_nutrition}")
    ingredient_embedding = aggregate_embeddings_max(embedding_dict[norm_ingredient])

    # Set allowed primary categories for swaps
    primary = INGREDIENT_PRIMARY_CATEGORIES.get(norm_ingredient, "other")
    allowed_primaries = set(CATEGORY_MAPPING["default_allowed_swaps"].get(primary, []))
    # Always allow vegetable swaps for flagged high-carb ingredients
    if restrictions and "max_carbohydrates_g_per_serving" in restrictions:
        allowed_primaries.add("vegetable")
    # Apply category exclusions from restrictions
    if restrictions and "exclude_categories" in restrictions:
        allowed_primaries -= set(restrictions["exclude_categories"])

    # Macronutrient threshold: skip swap if ingredient already meets restriction
    if restrictions and "max_carbohydrates_g_per_serving" in restrictions:
        if (
            original_nutrition is not None
            and "carbohydrates" in original_nutrition
            and original_nutrition["carbohydrates"] is not None
            and original_nutrition["carbohydrates"] <= restrictions["max_carbohydrates_g_per_serving"]
        ):
            print(f"DEBUG: Ingredient '{norm_ingredient}' already meets carb restriction, skipping swap.")
            return {"info": f"Ingredient already meets carb cutoff (<= {restrictions['max_carbohydrates_g_per_serving']}g carbs), no swap needed."}

    swap_candidates = []
    distances, indices = knn.k_nearest_neighbors(ingredient_embedding.reshape(1, -1))
    flat_indices = indices.flatten()
    flat_distances = 1 - distances.flatten() if len(distances.flatten()) > 0 else []

    if scaler is not None:
        flat_distances = scaler.transform(flat_distances.reshape(-1, 1)).flatten()

    for idx, dist in zip(flat_indices, flat_distances):
        if idx < len(ingredient_labels):
            substitute = ingredient_labels[idx]
            sub_primary = INGREDIENT_PRIMARY_CATEGORIES.get(substitute, "other")
            if sub_primary not in allowed_primaries:
                continue

            if restrictions and "exclude_categories" in restrictions and sub_primary in restrictions["exclude_categories"]:
                continue
            sub_nutrition = get_nutrition_profile(substitute)
            if restrictions and "max_carbohydrates_g_per_serving" in restrictions:
                if (
                    sub_nutrition is not None
                    and "carbohydrates" in sub_nutrition
                    and sub_nutrition["carbohydrates"] is not None
                    and sub_nutrition["carbohydrates"] > restrictions["max_carbohydrates_g_per_serving"]
                ):
                    continue
            if restrictions and "exclude_ingredients" in restrictions and substitute.lower() in [e.lower() for e in restrictions["exclude_ingredients"]]:
                continue
            if substitute == norm_ingredient:
                continue
            if not is_culinarily_valid(norm_ingredient, substitute):
                continue

            substitute_nutrition = get_nutrition_profile(substitute)
            nutrition_delta = calculate_nutrition_delta(original_nutrition, substitute_nutrition)
            foodbert_score = dist
            final_score = (0.8 * foodbert_score) - (0.2 * nutrition_delta)

            swap_candidates.append({
                "substitute": substitute,
                "score": final_score,
                "foodbert_score": foodbert_score,
                "nutrition_delta": nutrition_delta,
                "original_nutrition": original_nutrition,
                "substitute_nutrition": substitute_nutrition
            })

    # Sort candidates by score descending and take top 3
    swap_candidates = sorted(swap_candidates, key=lambda x: x["score"], reverse=True)[:3]

    if not swap_candidates:
        return {"error": "No suitable substitute found."}
    
    return {"ranked_swaps": swap_candidates}

import concurrent.futures

def swap_task(args):
    item, embedding_dict, knn_max, ingredient_labels, zscore_scaler, dietary_goal = args
    ingredient = item["ingredient"]
    swap_result = get_enhanced_swap(
        ingredient, embedding_dict, knn_max, ingredient_labels, scaler=zscore_scaler, dietary_goal=dietary_goal
    )
    return {
        "ingredient": ingredient,
        "rationale": item["rationale"],
        "swap_suggestion": swap_result
    }

def suggest_swaps(flagged_path, output_path_prefix="swap_suggestions_official", restrictions=None):
    with open(flagged_path, "r", encoding="utf-8") as f:
        flagged = json.load(f)
    
    embedding_dict_path = "foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert_combined.pkl"
    with open(embedding_dict_path, "rb") as f:
        embedding_dict = pickle.load(f)
    
    ingredient_labels = list(embedding_dict.keys())
    all_embeddings_max = [aggregate_embeddings_max(embedding_dict[label]) for label in ingredient_labels]
    all_embeddings_max = np.stack(all_embeddings_max)

    knn_max = ApproxKNNClassifier(all_ingredient_embeddings=all_embeddings_max, max_embedding_count=40)

    raw_scores = []
    for emb in all_embeddings_max:
        dists, _ = knn_max.k_nearest_neighbors(emb.reshape(1, -1))
        raw_scores.extend(1 - dists.flatten())
    raw_scores = np.array(raw_scores).reshape(-1, 1)
    zscore_scaler = StandardScaler().fit(raw_scores)

    swap_results = []
    for item in flagged:
        swap_result = get_enhanced_swap(
            item["ingredient"], embedding_dict, knn_max, ingredient_labels, scaler=zscore_scaler, restrictions=restrictions
        )
        swap_results.append({
            "ingredient": item["ingredient"],
            "rationale": item["rationale"],
            "swap_suggestion": swap_result
        })

    with open(f"{output_path_prefix}.json", "w", encoding="utf-8") as f:
        json.dump(swap_results, f, ensure_ascii=False, indent=2)
    print(f"Official swap suggestions saved to {output_path_prefix}.json")

if __name__ == "__main__":
    # Parse command-line arguments for restrictions and output_path_prefix
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Suggest ingredient swaps with category and dietary filtering.")
    parser.add_argument("--restrictions", type=str, default=None, help="JSON string or path to merged restriction rules")
    parser.add_argument("--output_path_prefix", type=str, default="swap_suggestions_official", help="Output file prefix")
    parser.add_argument("--flagged_path", type=str, default="workflow_flagged_ingredients.json", help="Flagged ingredients input file")
    args = parser.parse_args()

    # Load restrictions from JSON string or file
    restrictions = None
    if args.restrictions:
        try:
            if args.restrictions.endswith(".json"):
                with open(args.restrictions, "r", encoding="utf-8") as f:
                    restrictions = json.load(f)
            else:
                restrictions = json.loads(args.restrictions)
        except Exception as e:
            print(f"Error loading restrictions: {e}")
            restrictions = None

    suggest_swaps(args.flagged_path, output_path_prefix=args.output_path_prefix, restrictions=restrictions)
