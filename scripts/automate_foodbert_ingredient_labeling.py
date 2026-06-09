import json
import os
import sys
import time

# Allow importing shared modules (openfoodfacts_api, etc.) from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from openfoodfacts_api import get_product_metadata

# Step 1: Load and normalize FoodBERT ingredient list
def load_foodbert_ingredient_list(path):
    with open(path, "r", encoding="utf-8") as f:
        ingredients = json.load(f)
    # Normalize names
    normalized = [i.lower().strip().replace("-", " ").replace("_", " ") for i in ingredients]
    return normalized

# Step 2: Batch query Open Food Facts API for categories
def batch_query_openfoodfacts(ingredient_list, batch_size=100, sleep_time=60, output_path="outputs/foodbert_ingredient_categories.json"):
    results = {}
    failed = []
    for idx, ingredient in enumerate(ingredient_list):
        print(f"Querying Open Food Facts for: {ingredient} ({idx+1}/{len(ingredient_list)})")
        metadata = get_product_metadata(ingredient)
        if metadata is not None:
            categories = metadata.get("categories", [])
        else:
            categories = []
        results[ingredient] = categories
        # Respect API rate limit
        if (idx + 1) % batch_size == 0:
            print(f"Sleeping for {sleep_time} seconds to respect API rate limits...")
            time.sleep(sleep_time)
        # Log failed queries
        if not categories:
            failed.append(ingredient)
    # Save results
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved ingredient categories to {output_path}")
    # Save failed queries for manual/LLM review
    if failed:
        with open("outputs/foodbert_ingredient_categories_failed.json", "w", encoding="utf-8") as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)
        print(f"Saved failed ingredient queries to foodbert_ingredient_categories_failed.json")
    return results, failed

if __name__ == "__main__":
    # Example: Load FoodBERT ingredient list (should be a JSON array of ingredient names)
    ingredient_list_path = "foodBERT/foodbert_embeddings/data/used_ingredients_clean.json"
    ingredients = load_foodbert_ingredient_list(ingredient_list_path)
    batch_query_openfoodfacts(ingredients)
