import json
from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict
from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier
import numpy as np
import re

def normalize_ingredient_name(name):
    # Lowercase, strip, remove punctuation
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)
    return name

def aggregate_embeddings(emb_matrix):
    # Average across all sentence embeddings for an ingredient
    return np.mean(emb_matrix, axis=0)

def get_foodbert_swap(ingredient, embedding_dict, knn, ingredient_labels, threshold=0.7, top_n=1):
    norm_ingredient = normalize_ingredient_name(ingredient)
    if norm_ingredient not in embedding_dict:
        return {"error": f"Ingredient '{ingredient}' (normalized: '{norm_ingredient}') not in embedding vocabulary."}
    ingredient_embedding = aggregate_embeddings(embedding_dict[norm_ingredient])
    distances, indices = knn.k_nearest_neighbors(ingredient_embedding.reshape(1, -1))
    flat_indices = indices.flatten()
    flat_distances = flat_distances = flat_distances = 1 - flat_distances if len(flat_distances := distances.flatten()) > 0 else []
    for idx in flat_indices:
        if idx < len(ingredient_labels):
            substitute = ingredient_labels[idx]
            if substitute != norm_ingredient:
                score = float(flat_distances[list(flat_indices).index(idx)])
                if score < threshold:
                    return {
                        "substitute": substitute,
                        "score": score,
                        "manual_review": True,
                        "note": "Low similarity score; swap may not be appropriate."
                    }
                else:
                    return {"substitute": substitute, "score": score}
    return {"error": "No suitable substitute found."}

def suggest_swaps(flagged_path, output_path_prefix="swap_suggestions", threshold=0.7):
    with open(flagged_path, "r", encoding="utf-8") as f:
        flagged = json.load(f)
    embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
    ingredient_labels = list(embedding_dict.keys())
    # Aggregate embeddings for each ingredient
    all_embeddings = [aggregate_embeddings(embedding_dict[label]) for label in ingredient_labels]
    all_embeddings = np.stack(all_embeddings)
    knn = ApproxKNNClassifier(all_ingredient_embeddings=all_embeddings, max_embedding_count=100)
    swap_results = []
    for item in flagged:
        ingredient = item["ingredient"]
        swap_result = get_foodbert_swap(ingredient, embedding_dict, knn, ingredient_labels, threshold=threshold)
        swap_results.append({
            "ingredient": ingredient,
            "rationale": item["rationale"],
            "swap_suggestion": swap_result
        })
    with open(f"{output_path_prefix}.json", "w", encoding="utf-8") as f:
        json.dump(swap_results, f, ensure_ascii=False, indent=2)
    print(f"Swap suggestions saved to {output_path_prefix}.json")

if __name__ == "__main__":
    # Based on typical cosine similarity, 0.7 is a reasonable threshold for "good" similarity.
    suggest_swaps("workflow_flagged_ingredients.json", threshold=0.7)
