import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import json
import pickle
import numpy as np
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

from foodBERT.foodbert.helpers.prediction_model import PredictionModel, SimpleTokenizer

SENTENCE_FILE = "filtered_ingredient_sentences.json"
USED_INGREDIENTS_FILE = "foodBERT/foodbert_embeddings/data/used_ingredients_clean.json"
VOCAB_FILE = "foodBERT/foodbert/data/bert-base-cased-vocab.txt"
OUTPUT_FILE = "foodBERT/foodbert_embeddings/data/food_embeddings_dict_suggestic.pkl"

def _map_ingredients_to_input_ids():
    with Path(USED_INGREDIENTS_FILE).open() as f:
        ingredients = json.load(f)
    tokenizer = SimpleTokenizer(str(Path(VOCAB_FILE)))
    ingredient_ids = []
    for ingredient in ingredients:
        tokens = ['[CLS]'] + tokenizer.tokenize(ingredient) + ['[SEP]']
        ids = tokenizer.convert_tokens_to_ids(tokens)
        ingredient_ids.append(ids[1])  # Use the first token after [CLS] as the ingredient ID
    ingredient_ids_dict = dict(zip(ingredients, ingredient_ids))
    return ingredient_ids_dict

def main(max_sentence_count=40):
    with open(SENTENCE_FILE, "r", encoding="utf-8") as f:
        ingredient_sentences = json.load(f)

    all_ingredient_ids = _map_ingredients_to_input_ids()
    prediction_model = PredictionModel()
    food_to_embeddings_dict = defaultdict(list)

    for food, sentences in tqdm(ingredient_sentences.items(), desc="Suggestic Embeddings"):
        if not sentences:
            continue
        # Limit to max_sentence_count per ingredient
        sentences = sentences[:max_sentence_count]
        try:
            embeddings, ingredient_ids = prediction_model.predict_embeddings(sentences)
            embeddings_flat = embeddings.view((-1, prediction_model.config['hidden_size']))
            ingredient_ids_flat = ingredient_ids.flatten()
            food_id = all_ingredient_ids.get(food)
            if food_id is None:
                print(f"WARNING: Ingredient '{food}' not found in used_ingredients_clean.json.")
                continue
            food_embeddings = embeddings_flat[ingredient_ids_flat == food_id].cpu().numpy()
            if len(food_embeddings) == 0:
                print(f"WARNING: No embeddings found for ingredient '{food}' after filtering by token id.")
            food_to_embeddings_dict[food].extend(food_embeddings)
        except Exception as e:
            print(f"ERROR processing ingredient '{food}': {e}")

    # Only include ingredients with at least one embedding
    food_to_embeddings_dict = {k: np.stack(v) for k, v in food_to_embeddings_dict.items() if len(v) > 0}

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(food_to_embeddings_dict, f)

    print(f"Saved Suggestic embeddings to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
