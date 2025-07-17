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
with open("category_mapping_and_primary_tags.json", "r", encoding="utf-8") as f:
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

def get_nutrition_profile(ingredient):
    norm_ingredient = normalize_ingredient_name(ingredient)
    # Use Nutritionix reference for common spices and garlic
    if norm_ingredient in SPICE_NUTRITION:
        return SPICE_NUTRITION[norm_ingredient]
    # Otherwise use main lookup
    return get_food_nutrition_profile(norm_ingredient)

def get_enhanced_swap(ingredient, embedding_dict, knn, ingredient_labels, scaler=None, dietary_goal=None):
    norm_ingredient = normalize_ingredient_name(ingredient)
    print(f"DEBUG: Processing ingredient '{ingredient}' (normalized: '{norm_ingredient}')")
    if norm_ingredient not in embedding_dict:
        print(f"DEBUG: Ingredient '{norm_ingredient}' not found in embedding dictionary.")
        return {"error": f"Ingredient '{ingredient}' (normalized: '{norm_ingredient}') not in embedding vocabulary."}

    original_nutrition = get_nutrition_profile(norm_ingredient)
    print(f"DEBUG: Original nutrition for '{norm_ingredient}': {original_nutrition}")
    ingredient_embedding = aggregate_embeddings_max(embedding_dict[norm_ingredient])

  
  

    # ACTION ITEM 2 (updated): Skip swap if ingredient already has <=10g carbs per serving
    if dietary_goal == "low_carb":
        if (
            original_nutrition is not None
            and "carbohydrates" in original_nutrition
            and original_nutrition["carbohydrates"] is not None
            and original_nutrition["carbohydrates"] <= 10
        ):
            print(f"DEBUG: Ingredient '{norm_ingredient}' already has <=10g carbs, skipping swap.")
            return {"info": "Ingredient already meets low-carb cutoff (<=10g carbs), no swap needed."}

    distances, indices = knn.k_nearest_neighbors(ingredient_embedding.reshape(1, -1))
    flat_indices = indices.flatten()
    flat_distances = 1 - distances.flatten() if len(distances.flatten()) > 0 else []

    if scaler is not None:
        flat_distances = scaler.transform(flat_distances.reshape(-1, 1)).flatten()

    best_swap = {"score": -np.inf}
    
    for idx, dist in zip(flat_indices, flat_distances):
        if idx < len(ingredient_labels):
            substitute = ingredient_labels[idx]
            sub_primary = INGREDIENT_PRIMARY_CATEGORIES.get(substitute, "other")
            if sub_primary not in allowed_primaries:
                print(f"DEBUG: Substitute '{substitute}' filtered out by primary category '{sub_primary}'.")
                continue

            # Low-carb dietary goal: filter out substitutes with >=10g net carbs per serving
            if dietary_goal == "low_carb":
                sub_nutrition = get_nutrition_profile(substitute)
                # Exclude spices from low-carb filtering
                if substitute in COMMON_SPICES:
                    print(f"DEBUG: Substitute '{substitute}' is a spice, skipping low-carb filter.")
                elif (
                    sub_nutrition is not None
                    and "carbohydrates" in sub_nutrition
                    and sub_nutrition["carbohydrates"] is not None
                    and sub_nutrition["carbohydrates"] >= 10
                ):
                    print(f"DEBUG: Substitute '{substitute}' filtered out by low-carb rule (carbs: {sub_nutrition['carbohydrates']} >= 10).")
                    continue

            print(f"DEBUG: Considering substitute '{substitute}' for '{norm_ingredient}'")
            if substitute == norm_ingredient:
                print(f"DEBUG: Substitute '{substitute}' is the same as original. Skipping.")
                continue

            if not is_culinarily_valid(norm_ingredient, substitute):
                print(f"DEBUG: Substitute '{substitute}' failed culinary validity check. Skipping.")
                continue

            substitute_nutrition = get_nutrition_profile(substitute)
            print(f"DEBUG: Substitute nutrition for '{substitute}': {substitute_nutrition}")
            nutrition_delta = calculate_nutrition_delta(original_nutrition, substitute_nutrition)
            print(f"DEBUG: Nutrition delta for '{substitute}': {nutrition_delta}")
            
            # Weighted score
            foodbert_score = dist
            final_score = (0.8 * foodbert_score) - (0.2 * nutrition_delta)
            print(f"DEBUG: Final score for '{substitute}': {final_score}")

            if final_score > best_swap["score"]:
                best_swap = {
                    "substitute": substitute,
                    "score": final_score,
                    "foodbert_score": foodbert_score,
                    "nutrition_delta": nutrition_delta,
                    "original_nutrition": original_nutrition,
                    "substitute_nutrition": substitute_nutrition
                }

    if best_swap["score"] == -np.inf:
        print(f"DEBUG: No suitable substitute found for '{norm_ingredient}'.")
        return {"error": "No suitable substitute found."}
    
    print(f"DEBUG: Best swap for '{norm_ingredient}': {best_swap}")
    return best_swap

def suggest_swaps(flagged_path, output_path_prefix="swap_suggestions_official", dietary_goal=None):
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
        ingredient = item["ingredient"]
        swap_result = get_enhanced_swap(
            ingredient, embedding_dict, knn_max, ingredient_labels, scaler=zscore_scaler, dietary_goal=dietary_goal
        )
        swap_results.append({
            "ingredient": ingredient,
            "rationale": item["rationale"],
            "swap_suggestion": swap_result
        })
        
    with open(f"{output_path_prefix}.json", "w", encoding="utf-8") as f:
        json.dump(swap_results, f, ensure_ascii=False, indent=2)
    print(f"Official swap suggestions saved to {output_path_prefix}.json")

if __name__ == "__main__":
    # Parse command-line arguments for dietary_goal and output_path_prefix
    import argparse
    parser = argparse.ArgumentParser(description="Suggest ingredient swaps with category and dietary filtering.")
    parser.add_argument("--dietary_goal", type=str, default=None, help="Special dietary goal (e.g., low_carb)")
    parser.add_argument("--output_path_prefix", type=str, default="swap_suggestions_official", help="Output file prefix")
    parser.add_argument("--flagged_path", type=str, default="workflow_flagged_ingredients.json", help="Flagged ingredients input file")
    args = parser.parse_args()

    suggest_swaps(args.flagged_path, output_path_prefix=args.output_path_prefix, dietary_goal=args.dietary_goal)
