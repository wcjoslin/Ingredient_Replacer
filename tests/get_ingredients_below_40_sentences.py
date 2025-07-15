import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict

def get_ingredients_below_threshold(threshold=40):
    embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
    below_threshold = {k: int(v.shape[0]) for k, v in embedding_dict.items() if v.shape[0] < threshold}
    with open("tests/ingredients_below_40_sentences.json", "w", encoding="utf-8") as f:
        json.dump(below_threshold, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(below_threshold)} ingredients below {threshold} sentences to tests/ingredients_below_40_sentences.json")

if __name__ == "__main__":
    get_ingredients_below_threshold(threshold=40)
