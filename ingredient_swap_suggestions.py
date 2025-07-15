import json
import pickle
import numpy as np
import re
from sklearn.preprocessing import StandardScaler

from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier

def normalize_ingredient_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)
    return name

def aggregate_embeddings_max(emb_matrix):
    return np.max(emb_matrix, axis=0)

def get_foodbert_swap(ingredient, embedding_dict, knn, ingredient_labels, threshold=0.7, scaler=None):
    norm_ingredient = normalize_ingredient_name(ingredient)
    if norm_ingredient not in embedding_dict:
        return {"error": f"Ingredient '{ingredient}' (normalized: '{norm_ingredient}') not in embedding vocabulary."}
    ingredient_embedding = aggregate_embeddings_max(embedding_dict[norm_ingredient])

    distances, indices = knn.k_nearest_neighbors(ingredient_embedding.reshape(1, -1))
    flat_indices = indices.flatten()
    flat_distances = 1 - distances.flatten() if len(distances.flatten()) > 0 else []

    # Z-score normalization
    if scaler is not None:
        flat_distances = scaler.transform(flat_distances.reshape(-1, 1)).flatten()

    for idx in flat_indices:
        if idx < len(ingredient_labels):
            substitute = ingredient_labels[idx]
            if substitute != norm_ingredient:
                score = float(flat_distances[list(flat_indices).index(idx)])
                return {"substitute": substitute, "score": score, "aggregation": "max", "scoring": "zscore"}
    return {"error": "No suitable substitute found."}

def suggest_swaps(flagged_path, output_path_prefix="swap_suggestions_official", threshold=0.7):
    with open(flagged_path, "r", encoding="utf-8") as f:
        flagged = json.load(f)
    embedding_dict_path = "foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert_combined.pkl"
    with open(embedding_dict_path, "rb") as f:
        embedding_dict = pickle.load(f)
    ingredient_labels = list(embedding_dict.keys())
    # Aggregate embeddings for each ingredient (max)
    all_embeddings_max = [aggregate_embeddings_max(embedding_dict[label]) for label in ingredient_labels]
    all_embeddings_max = np.stack(all_embeddings_max)

    knn_max = ApproxKNNClassifier(all_ingredient_embeddings=all_embeddings_max, max_embedding_count=40)

    # Fit z-score scaler on all pairwise similarities
    raw_scores = []
    for emb in all_embeddings_max:
        dists, _ = knn_max.k_nearest_neighbors(emb.reshape(1, -1))
        raw_scores.extend(1 - dists.flatten())
    raw_scores = np.array(raw_scores).reshape(-1, 1)
    zscore_scaler = StandardScaler().fit(raw_scores)

    swap_results = []
    for item in flagged:
        ingredient = item["ingredient"]
        swap_result = get_foodbert_swap(
            ingredient, embedding_dict, knn_max, ingredient_labels,
            threshold=threshold, scaler=zscore_scaler
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
    suggest_swaps("workflow_flagged_ingredients.json", threshold=0.7)
