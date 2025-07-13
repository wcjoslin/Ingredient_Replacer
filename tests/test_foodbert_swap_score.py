import numpy as np
from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict

def cosine_similarity(a, b):
    a = a.flatten()
    b = b.flatten()
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def aggregate_embeddings(emb_matrix):
    return np.mean(emb_matrix, axis=0)

if __name__ == "__main__":
    embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
    ingr_a = "penne"
    ingr_b = "zucchini noodles"
    # Try alternative names for zucchini noodles if not found
    if ingr_b not in embedding_dict:
        ingr_b = "zucchini"
    if ingr_a in embedding_dict and ingr_b in embedding_dict:
        emb_a = aggregate_embeddings(embedding_dict[ingr_a])
        emb_b = aggregate_embeddings(embedding_dict[ingr_b])
        sim = cosine_similarity(emb_a, emb_b)
        print(f"FoodBERT similarity score for swap '{ingr_a}' -> '{ingr_b}': {sim:.4f}")
    else:
        print(f"Missing embedding for {ingr_a} or {ingr_b}")
