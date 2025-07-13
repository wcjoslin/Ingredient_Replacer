from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict

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
    print("Embedding shapes for flagged ingredients:")
    for ingr in ingredients:
        if ingr in embedding_dict:
            print(f"{ingr}: {embedding_dict[ingr].shape}")
        else:
            print(f"{ingr}: MISSING")
