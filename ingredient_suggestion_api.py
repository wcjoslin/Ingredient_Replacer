# ingredient_suggestion_api.py
# FastAPI endpoint for dynamic foodBERT-powered ingredient swaps and robust enrichment

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

from ingredient_swap_suggestions import get_enhanced_swap, COMMON_SPICES
from dietary_restriction_analysis import analyze_dietary_restrictions
from ingredient_workflow import map_ingredients_to_foodbert

# Import robust enrichment logic
from ingredient_data_enrichment import enrich_recipe_ingredients

app = FastAPI(title="Multi-Ingredient Suggestion API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load all required data/models ONCE at startup
with open("foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert_combined.pkl", "rb") as f:
    embedding_dict = pickle.load(f)
ingredient_labels = list(embedding_dict.keys())
all_embeddings_max = [np.max(embedding_dict[label], axis=0) for label in ingredient_labels]
all_embeddings_max = np.stack(all_embeddings_max)
from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier
knn_max = ApproxKNNClassifier(all_ingredient_embeddings=all_embeddings_max, max_embedding_count=40)
raw_scores = []
for emb in all_embeddings_max:
    dists, _ = knn_max.k_nearest_neighbors(emb.reshape(1, -1))
    raw_scores.extend(1 - dists.flatten())
raw_scores = np.array(raw_scores).reshape(-1, 1)
zscore_scaler = StandardScaler().fit(raw_scores)

with open("ingredient_primary_categories.json", "r", encoding="utf-8") as cat_file:
    primary_categories = json.load(cat_file)

# Load dietary restriction presets
with open("dietary_restriction_presets.json", "r", encoding="utf-8") as f:
    restriction_presets = json.load(f)

# Load foodBERT category keys for each ingredient for raw category logic
with open("foodbert_ingredient_categories_merged.json", "r", encoding="utf-8") as f:
    foodbert_categories = json.load(f)

def format_category_display(cat_key):
    if cat_key.startswith("en:"):
        cat_key = cat_key[3:]
    return cat_key.replace("-", " ").replace("_", " ").title()

def merge_restriction_rules(diet_ids: List[str]):
    merged_rules = {}
    for rid in diet_ids:
        preset = next((p for p in restriction_presets if p["id"] == rid), None)
        if preset:
            for k, v in preset["rules"].items():
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
    return merged_rules

@app.get("/suggestions")
def suggestions_get():
    return JSONResponse(content={"error": "Use POST for /suggestions. This endpoint only supports POST requests with a JSON body containing ingredients and diets."}, status_code=405)

@app.post("/suggestions")
async def get_suggestions_post(request: Request):
    """
    Accepts a POST request with a JSON body:
    {
        "ingredients": ["ingredient1", "ingredient2", ...],
        "diets": ["vegan", "glutenfree", ...]  # optional
    }
    Returns swap suggestions for the provided ingredients, filtered by diets if specified.
    """
    body = await request.json()
    raw_ingredients = body.get("ingredients", [])
    diets = body.get("diets", [])
    restrictions = merge_restriction_rules(diets)

    # Debug: Print received diets
    print("Received diets:", diets)

    # Step 0: Normalize and map ingredients to foodBERT vocabulary
    mapped_ingredients = map_ingredients_to_foodbert(raw_ingredients)
    print(f"\n--- MAPPED INGREDIENTS ---\n{mapped_ingredients}\n")

    # Step 1: Robust enrichment (nutrition, categories, dietary flags, error handling)
    enriched_dict = enrich_recipe_ingredients(mapped_ingredients)
    enriched_data = []
    for ingr in mapped_ingredients:
        nutrition = {}
        # Use raw foodBERT category keys for logic
        raw_category_keys = foodbert_categories.get(ingr.lower().strip(), [])
        dietary_flags = []
        # Human-friendly display categories
        display_categories = [format_category_display(cat) for cat in raw_category_keys]
        for bp in enriched_dict.get(ingr, []):
            lower_bp = bp.lower()
            if lower_bp.startswith("calories"):
                try:
                    nutrition["calories"] = float(bp.split(":")[1].strip())
                except Exception:
                    pass
            elif lower_bp.startswith("protein"):
                try:
                    nutrition["protein"] = float(bp.split(":")[1].strip())
                except Exception:
                    pass
            elif lower_bp.startswith("carbs"):
                try:
                    nutrition["carbohydrates"] = float(bp.split(":")[1].strip())
                except Exception:
                    pass
            elif lower_bp.startswith("fat"):
                try:
                    nutrition["fat"] = float(bp.split(":")[1].strip())
                except Exception:
                    pass
            elif bp.endswith("-friendly") or bp.startswith("Not "):
                dietary_flags.append(bp.strip())
        enriched_data.append({
            "ingredient": ingr,
            "nutrition": nutrition,
            "categories": raw_category_keys,  # Use raw keys for logic and rules
            "display_categories": display_categories,  # User-friendly for UI
            "dietary_flags": dietary_flags
        })
    print(f"\n--- ENRICHED INGREDIENT DATA ---\n{enriched_data}\n")

    # Step 2: Flag ingredients based on restrictions (uses raw category keys)
    flagged_ingredients = analyze_dietary_restrictions(enriched_data, restrictions)
    print("--- FLAGGED INGREDIENTS ---")
    for item in flagged_ingredients:
        print(item["ingredient"], item.get("dietary_flags", []))

    # Step 3: Filter flagged ingredients (remove spices, low-carb, missing category)
    filtered_flagged = []
    for item in flagged_ingredients:
        name = item["ingredient"].lower().strip()
        if name in COMMON_SPICES:
            continue
        nutrition = item.get("nutrition", {})
        # Only filter for low-carb if requested
        if "lowcarb" in diets and nutrition and nutrition.get("carbohydrates", 0) <= 10:
            continue
        target_category = primary_categories.get(name)
        if not target_category:
            continue
        filtered_flagged.append(item)
    print(f"\n--- FILTERED FLAGGED INGREDIENTS ---\n{filtered_flagged}\n")

    # Step 4: Get swap suggestions for flagged ingredients
    results = []
    for item in filtered_flagged:
        swap_result = get_enhanced_swap(
            item["ingredient"], embedding_dict, knn_max, ingredient_labels, scaler=zscore_scaler, restrictions=restrictions
        )
        results.append({
            "original": item["ingredient"],
            "categories": item.get("categories", []),  # raw keys
            "display_categories": item.get("display_categories", []),  # for UI
            "dietary_flags": item.get("dietary_flags", []),
            "swap_suggestion": swap_result
        })
    print(f"\n--- FINAL SWAP RESULTS ---\n{results}\n")

    return JSONResponse(content={"suggestions": results})
