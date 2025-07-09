import pickle

pickle_path = "foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert.pkl"
ingredient = "olive oil"

with open(pickle_path, "rb") as f:
    data = pickle.load(f)

if ingredient in data:
    print(f"'{ingredient}' is present in the embedding dictionary.")
    print(f"Embedding shape: {data[ingredient].shape}")
else:
    print(f"'{ingredient}' is NOT present in the embedding dictionary.")
    print(f"Available keys (sample): {list(data.keys())[:10]}")
