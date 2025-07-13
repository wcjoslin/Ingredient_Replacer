import numpy as np
from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict

def cosine_similarity(a, b):
    a = a.flatten()
    b = b.flatten()
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

if __name__ == "__main__":
    embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
    ingredients = [
        "penne",
        "parmesan cheese",
        "garlic",
        "olive oil",
        "baby spinach leaves",
        "basil leaves"
    ]
    print("Cosine similarities between flagged ingredients:")
    for i in range(len(ingredients)):
        for j in range(i+1, len(ingredients)):
            ingr_a = ingredients[i]
            ingr_b = ingredients[j]
            if ingr_a in embedding_dict and ingr_b in embedding_dict:
                sim = cosine_similarity(embedding_dict[ingr_a], embedding_dict[ingr_b])
                print(f"{ingr_a} vs {ingr_b}: {sim:.4f}")
            else:
                print(f"Missing embedding for {ingr_a} or {ingr_b}")
