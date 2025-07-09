print("DEBUG: Script started")
import json
import pickle
import random
import re
from collections import defaultdict
from pathlib import Path

print("DEBUG: Imported standard libraries")

import numpy as np
import torch
print("DEBUG: Imported numpy and torch")
from tqdm import tqdm

print("DEBUG: Imported tqdm")

from foodBERT.foodbert.helpers.prediction_model import PredictionModel, SimpleTokenizer
print("DEBUG: Imported PredictionModel and SimpleTokenizer")

def _generate_food_sentence_dict():
    with Path('foodBERT/foodbert_embeddings/data/used_ingredients_clean.json').open() as f:
        food_items = json.load(f)
        food_items_set = set(food_items)

    with Path('foodBERT/foodbert/data/train_instructions.txt').open() as f:
        train_instruction_sentences = f.read().splitlines()
        # remove overlong sentences
        train_instruction_sentences = [s for s in train_instruction_sentences if len(s.split()) <= 100]

    with Path('foodBERT/foodbert/data/test_instructions.txt').open() as f:
        test_instruction_sentences = f.read().splitlines()
        # remove overlong sentences
        test_instruction_sentences = [s for s in test_instruction_sentences if len(s.split()) <= 100]

    instruction_sentences = train_instruction_sentences + test_instruction_sentences

    food_to_sentences_dict = defaultdict(list)
    for sentence in instruction_sentences:
        for food in food_items_set:
            if food in sentence:
                food_to_sentences_dict[food].append(sentence)

    return food_to_sentences_dict

def _random_sample_with_min_count(population, k):
    if len(population) <= k:
        return population
    else:
        return random.sample(population, k)

def sample_random_sentence_dict(max_sentence_count):
    food_to_sentences_dict = _generate_food_sentence_dict()
    # only keep max_sentence_count randomly selected sentences
    food_to_sentences_dict_random_samples = {
        food: _random_sample_with_min_count(sentences, max_sentence_count)
        for food, sentences in food_to_sentences_dict.items()
    }
    return food_to_sentences_dict_random_samples

def _map_ingredients_to_input_ids():
    with Path('foodBERT/foodbert_embeddings/data/used_ingredients_clean.json').open() as f:
        ingredients = json.load(f)
    tokenizer = SimpleTokenizer(str(Path('foodBERT/foodbert/data/bert-base-cased-vocab.txt')))
    ingredient_ids = []
    for ingredient in ingredients:
        tokens = ['[CLS]'] + tokenizer.tokenize(ingredient) + ['[SEP]']
        ids = tokenizer.convert_tokens_to_ids(tokens)
        ingredient_ids.append(ids[1])  # Use the first token after [CLS] as the ingredient ID
    ingredient_ids_dict = dict(zip(ingredients, ingredient_ids))
    return ingredient_ids_dict

def _merge_synonmys(food_to_embeddings_dict, max_sentence_count):
    synonmy_replacements_path = Path('foodBERT/foodbert_embeddings/data/synonmy_replacements.json')
    if synonmy_replacements_path.exists():
        with synonmy_replacements_path.open() as f:
            synonmy_replacements = json.load(f)
    else:
        synonmy_replacements = {}

    merged_dict = defaultdict(list)
    # Merge ingredients
    for key, value in food_to_embeddings_dict.items():
        if key in synonmy_replacements:
            key_to_use = synonmy_replacements[key]
        else:
            key_to_use = key

        merged_dict[key_to_use].append(value)

    merged_dict = {k: np.concatenate(v) for k, v in merged_dict.items()}
    # When embedding count exceeds maximum allowed, reduce back to requested count
    for key, value in merged_dict.items():
        if len(value) > max_sentence_count:
            index = np.random.choice(value.shape[0], max_sentence_count, replace=False)
            new_value = value[index]
            merged_dict[key] = new_value

    return merged_dict

def generate_food_embedding_dict(max_sentence_count):
    '''
    Creates a dict where the keys are the ingredients and the values are a list of embeddings.
    '''
    food_to_embeddings_dict_path = Path('foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert.pkl')
    if food_to_embeddings_dict_path.exists():
        with food_to_embeddings_dict_path.open('rb') as f:
            food_to_embeddings_dict = pickle.load(f)

        # delete keys if we deleted ingredients
        old_ingredients = set(food_to_embeddings_dict.keys())
        with Path('foodBERT/foodbert_embeddings/data/used_ingredients_clean.json').open() as f:
            new_ingredients = set(json.load(f))

        keys_to_delete = old_ingredients.difference(new_ingredients)
        for key in keys_to_delete:
            food_to_embeddings_dict.pop(key, None)

        # merge new synonyms
        food_to_embeddings_dict = _merge_synonmys(food_to_embeddings_dict, max_sentence_count)

        with food_to_embeddings_dict_path.open('wb') as f:
            pickle.dump(food_to_embeddings_dict, f)

        return food_to_embeddings_dict

    print('Sampling Random Sentences')
    food_to_sentences_dict_random_samples = sample_random_sentence_dict(max_sentence_count=max_sentence_count)
    # Debug: print ingredients with no matched sentences
    for food, sentences in food_to_sentences_dict_random_samples.items():
        if not sentences:
            print(f"WARNING: No matched sentences for ingredient '{food}'")

    food_to_embeddings_dict = defaultdict(list)
    print('Mapping Ingredients to Input Ids')
    all_ingredient_ids = _map_ingredients_to_input_ids()

    prediction_model = PredictionModel()
    for food, sentences in tqdm(food_to_sentences_dict_random_samples.items(), 
                              total=len(food_to_sentences_dict_random_samples),
                              desc='Calculating Embeddings for Food items'):
        if not sentences:
            continue  # Skip ingredients with no sentences
        try:
            embeddings, ingredient_ids = prediction_model.predict_embeddings(sentences)
            # get embedding of food word
            embeddings_flat = embeddings.view((-1, prediction_model.config['hidden_size']))
            ingredient_ids_flat = ingredient_ids.flatten()
            food_id = all_ingredient_ids[food]
            food_embeddings = embeddings_flat[ingredient_ids_flat == food_id].cpu().numpy()
            if len(food_embeddings) == 0:
                print(f"WARNING: No embeddings found for ingredient '{food}' after filtering by token id.")
            food_to_embeddings_dict[food].extend(food_embeddings)
        except Exception as e:
            print(f"ERROR processing ingredient '{food}': {e}")

    # Only include ingredients with at least one embedding
    food_to_embeddings_dict = {k: np.stack(v) for k, v in food_to_embeddings_dict.items() if len(v) > 0}
    # Clean synonmy
    food_to_embeddings_dict = _merge_synonmys(food_to_embeddings_dict, max_sentence_count)

    with food_to_embeddings_dict_path.open('wb') as f:
        pickle.dump(food_to_embeddings_dict, f)

    return food_to_embeddings_dict
