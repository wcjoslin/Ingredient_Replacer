import json
import pickle
import numpy as np
import re
import sys
# Removed scikit-learn dependency for normalization

from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier
from src.nutritional_analysis import calculate_nutrition_delta
from src.culinary_rules import is_culinarily_valid
from src.usda_api import get_food_nutrition_profile

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

# --- NEW: Load precomputed foodBERT swap cache ---
try:
    with open("foodBERT/foodbert_embeddings/foodbert_swap_cache.json", "r", encoding="utf-8") as f:
        PRECOMPUTED_FOODBERT_CACHE = json.load(f)
except Exception as e:
    PRECOMPUTED_FOODBERT_CACHE = {}
    print(f"WARNING: Could not load foodBERT swap cache: {e}")

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

def get_enhanced_swap(ingredient, embedding_dict=None, knn=None, ingredient_labels=None, scaler=None, restrictions=None):
    norm_ingredient = normalize_ingredient_name(ingredient)
    # --- NEW: Use precomputed cache if available ---
    if norm_ingredient in PRECOMPUTED_FOODBERT_CACHE:
        cached_swaps = PRECOMPUTED_FOODBERT_CACHE[norm_ingredient]
        if cached_swaps is None:
            return {"error": "No suitable substitute found in cache."}
        # Format cache data to match API output
        ranked_swaps = []
        for swap in cached_swaps:
            substitute, score = swap
            substitute_nutrition = get_nutrition_profile(substitute)
            original_nutrition = get_nutrition_profile(norm_ingredient)
            nutrition_delta = calculate_nutrition_delta(original_nutrition, substitute_nutrition)
            ranked_swaps.append({
                "substitute": substitute,
                "score": score,
                "foodbert_score": score,
                "nutrition_delta": nutrition_delta,
                "original_nutrition": original_nutrition,
                "substitute_nutrition": substitute_nutrition
            })
        return {"ranked_swaps": ranked_swaps}
    # --- Fallback: Live model inference (should not be used in production) ---
    print(f"WARNING: Ingredient '{norm_ingredient}' not found in precomputed cache. Live inference is disabled.")
    return {"error": "No swap suggestion available for this ingredient in cache."}

# The rest of the file remains unchanged (other functions, CLI, etc.)
