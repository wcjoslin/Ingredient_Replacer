"""
Precompute foodBERT swap suggestions for all ingredients in used_ingredients.json.
Saves results to foodBERT/foodbert_embeddings/foodbert_swap_cache.json.
References: generate_substitutes.py
"""

import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generate_substitutes import get_nearest_N_neigbours, generate_food_embedding_dict, ApproxKNNClassifier
import numpy as np

USED_INGREDIENTS_PATH = "foodBERT/foodbert/data/used_ingredients.json"
CACHE_PATH = "foodBERT/foodbert_embeddings/foodbert_swap_cache.json"

def main():
    with open(USED_INGREDIENTS_PATH, "r", encoding="utf-8") as f:
        ingredients = json.load(f)

    # Load embeddings and classifier (mirroring generate_substitutes.py main)
    max_embedding_count = 100
    ingredients_to_embeddings = generate_food_embedding_dict(max_sentence_count=max_embedding_count)

    all_ingredient_embeddings = []
    all_ingredient_labels = []

    for key, value in ingredients_to_embeddings.items():
        all_ingredient_embeddings.append(value)
        all_ingredient_labels.extend([key] * len(value))

    all_ingredient_embeddings = np.concatenate(all_ingredient_embeddings)
    all_ingredient_labels = np.stack(all_ingredient_labels)

    knn_classifier = ApproxKNNClassifier(all_ingredient_embeddings=all_ingredient_embeddings,
                                         max_embedding_count=max_embedding_count)

    cache = {}
    print(f"Starting swap suggestion generation for {len(ingredients)} ingredients...")
    for idx, ingredient in enumerate(ingredients):
        if ingredient not in ingredients_to_embeddings:
            cache[ingredient] = None
            print(f"[{idx+1}/{len(ingredients)}] {ingredient}: No embedding found, skipping.")
            continue
        swap_result = get_nearest_N_neigbours(
            ingredient_name=ingredient,
            ingredients_to_embeddings=ingredients_to_embeddings,
            all_ingredient_labels=all_ingredient_labels,
            knn_classifier=knn_classifier
        )
        cache[ingredient] = swap_result
        print(f"[{idx+1}/{len(ingredients)}] {ingredient}: Swap result computed.")

    print(f"Writing cache to {CACHE_PATH} ...")
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    print("Cache file written successfully.")

if __name__ == "__main__":
    main()
