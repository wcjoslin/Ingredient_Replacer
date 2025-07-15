print("DEBUG: Script started")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import json
import pickle
import random
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from tqdm import tqdm

print("DEBUG: Imported libraries")

from foodBERT.foodbert.helpers.prediction_model import PredictionModel, SimpleTokenizer

def normalize_ingredient_name(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)
    return name

def _generate_food_sentence_dict_combined():
    print("DEBUG: Entered _generate_food_sentence_dict_combined")
    food_items_path = Path('foodBERT/foodbert_embeddings/data/used_ingredients_clean.json')
    with food_items_path.open() as f:
        food_items = json.load(f)
    food_items_set = set([normalize_ingredient_name(f) for f in food_items])
    print(f"DEBUG: Loaded {len(food_items_set)} ingredients")

    train_path = Path('foodBERT/foodbert/data/train_instructions.txt')
    test_path = Path('foodBERT/foodbert/data/test_instructions.txt')
    train_instruction_sentences = []
    test_instruction_sentences = []
    if train_path.exists():
        with train_path.open() as f:
            train_instruction_sentences = f.read().splitlines()
            train_instruction_sentences = [s for s in train_instruction_sentences if len(s.split()) <= 100]
    if test_path.exists():
        with test_path.open() as f:
            test_instruction_sentences = f.read().splitlines()
            test_instruction_sentences = [s for s in test_instruction_sentences if len(s.split()) <= 100]
    instruction_sentences = train_instruction_sentences + test_instruction_sentences
    print(f"DEBUG: Loaded {len(instruction_sentences)} instruction sentences")

    suggestic_path = Path('filtered_ingredient_sentences.json')
    suggestic_sentences_dict = {}
    if suggestic_path.exists():
        with suggestic_path.open(encoding="utf-8") as f:
            suggestic_sentences_dict = json.load(f)
    print(f"DEBUG: Loaded {len(suggestic_sentences_dict)} suggestic ingredients")
    suggestic_sentences_dict = {normalize_ingredient_name(k): v for k, v in suggestic_sentences_dict.items()}

    food_to_sentences_dict = defaultdict(list)
    for sentence in instruction_sentences:
        for food in food_items_set:
            if food in normalize_ingredient_name(sentence):
                food_to_sentences_dict[food].append(sentence)
    for food, sentences in suggestic_sentences_dict.items():
        food_to_sentences_dict[food].extend(sentences)
    print(f"DEBUG: Built combined sentence dict with {len(food_to_sentences_dict)} ingredients")
    return food_to_sentences_dict

def _random_sample_with_min_count(population, k):
    if len(population) <= k:
        return population
    else:
        return random.sample(population, k)

def sample_random_sentence_dict_combined(max_sentence_count):
    print("DEBUG: Entered sample_random_sentence_dict_combined")
    food_to_sentences_dict = _generate_food_sentence_dict_combined()
    food_to_sentences_dict_random_samples = {
        food: _random_sample_with_min_count(sentences, max_sentence_count)
        for food, sentences in food_to_sentences_dict.items()
    }
    print(f"DEBUG: Sampled sentences for {len(food_to_sentences_dict_random_samples)} ingredients")
    return food_to_sentences_dict_random_samples

def _map_ingredients_to_input_ids():
    print("DEBUG: Entered _map_ingredients_to_input_ids")
    with Path('foodBERT/foodbert_embeddings/data/used_ingredients_clean.json').open() as f:
        ingredients = json.load(f)
    tokenizer = SimpleTokenizer(str(Path('foodBERT/foodbert/data/bert-base-cased-vocab.txt')))
    ingredient_ids = []
    for ingredient in ingredients:
        tokens = ['[CLS]'] + tokenizer.tokenize(ingredient) + ['[SEP]']
        ids = tokenizer.convert_tokens_to_ids(tokens)
        ingredient_ids.append(ids[1])
    ingredient_ids_dict = dict(zip([normalize_ingredient_name(i) for i in ingredients], ingredient_ids))
    print(f"DEBUG: Mapped {len(ingredient_ids_dict)} ingredient IDs")
    return ingredient_ids_dict

def generate_food_embedding_dict(max_sentence_count):
    print("DEBUG: Entered generate_food_embedding_dict")
    food_to_embeddings_dict_path = Path('foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert_combined.pkl')
    print('Sampling Random Sentences (Combined)')
    food_to_sentences_dict_random_samples = sample_random_sentence_dict_combined(max_sentence_count=max_sentence_count)
    for food, sentences in food_to_sentences_dict_random_samples.items():
        if not sentences:
            print(f"WARNING: No matched sentences for ingredient '{food}'")

    food_to_embeddings_dict = defaultdict(list)
    print('Mapping Ingredients to Input Ids')
    all_ingredient_ids = _map_ingredients_to_input_ids()

    prediction_model = PredictionModel()
    print("DEBUG: PredictionModel initialized")
    for food, sentences in tqdm(food_to_sentences_dict_random_samples.items(), 
                              total=len(food_to_sentences_dict_random_samples),
                              desc='Calculating Embeddings for Food items'):
        if not sentences:
            continue
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

    food_to_embeddings_dict = {k: np.stack(v) for k, v in food_to_embeddings_dict.items() if len(v) > 0}

    output_dir = food_to_embeddings_dict_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with food_to_embeddings_dict_path.open('wb') as f:
        pickle.dump(food_to_embeddings_dict, f)

    print(f"Saved combined embeddings to {food_to_embeddings_dict_path.resolve()}")

    return food_to_embeddings_dict

print("DEBUG: End of script file")

if __name__ == "__main__":
    print("DEBUG: Running as main")
    generate_food_embedding_dict(max_sentence_count=40)
