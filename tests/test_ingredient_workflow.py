import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../foodBERT")))

import pytest
from ingredient_workflow import normalize_ingredient_string, fuzzy_match_ingredient, map_ingredients_to_foodbert
from dietary_restriction_analysis import analyze_dietary_restrictions
from ingredient_swap_suggestions import get_enhanced_swap

def test_normalize_ingredient_string():
    assert normalize_ingredient_string("¾ cup parmesan cheese") == "parmesan cheese"
    assert normalize_ingredient_string("½ teaspoon salt") == "salt"
    assert normalize_ingredient_string("egg") == "egg"
    assert normalize_ingredient_string("mozzarella cheese") == "mozzarella cheese"
    assert normalize_ingredient_string("▢ 1 tablespoon olive oil") == "olive oil"
    assert normalize_ingredient_string("¼ tsp pepper") == "tsp pepper"
    assert normalize_ingredient_string("¾ lb. ground beef") == "ground beef"
    assert normalize_ingredient_string("cucumber cut into pieces") == "cucumber"
    assert normalize_ingredient_string("2 cups shredded cheddar cheese") == "cheddar cheese"
    assert normalize_ingredient_string("¼ teaspoon black pepper") == "black pepper"
    assert normalize_ingredient_string("onion, chopped") == "onion"

def test_fuzzy_match_ingredient():
    vocab = {"parmesan cheese", "salt", "egg", "mozzarella cheese", "olive oil", "ground beef"}
    assert fuzzy_match_ingredient("parmesan cheese", vocabulary=vocab, cutoff=0.6) == "parmesan cheese"
    assert fuzzy_match_ingredient("salt", vocabulary=vocab, cutoff=0.6) == "salt"
    assert fuzzy_match_ingredient("egg", vocabulary=vocab, cutoff=0.6) == "egg"
    assert fuzzy_match_ingredient("mozzarella cheese", vocabulary=vocab, cutoff=0.6) == "mozzarella cheese"
    assert fuzzy_match_ingredient("olive oil", vocabulary=vocab, cutoff=0.6) == "olive oil"
    assert fuzzy_match_ingredient("ground beef", vocabulary=vocab, cutoff=0.6) == "ground beef"
    assert fuzzy_match_ingredient("unknown ingredient", vocabulary=vocab, cutoff=0.6) == ""

def test_map_ingredients_to_foodbert():
    vocab = {"parmesan cheese", "salt", "egg", "mozzarella cheese", "olive oil", "ground beef", "cucumber", "cheddar cheese", "black pepper", "onion"}
    ingredients = [
        "¾ cup parmesan cheese",
        "½ teaspoon salt",
        "egg",
        "mozzarella cheese",
        "▢ 1 tablespoon olive oil",
        "¾ lb. ground beef",
        "cucumber cut into pieces",
        "2 cups shredded cheddar cheese",
        "¼ teaspoon black pepper",
        "onion, chopped",
        "unknown ingredient"
    ]
    def patched_fuzzy_match_ingredient(cleaned, vocabulary=vocab, cutoff=0.6):
        return fuzzy_match_ingredient(cleaned, vocabulary=vocab, cutoff=cutoff)
    mapped = []
    for raw in ingredients:
        norm = normalize_ingredient_string(raw)
        core = extract_core_ingredient_spacy(norm)
        match = patched_fuzzy_match_ingredient(core)
        if match:
            mapped.append(match)
    assert mapped == [
        "parmesan cheese",
        "salt",
        "egg",
        "mozzarella cheese",
        "olive oil",
        "ground beef",
        "cucumber",
        "cheddar cheese",
        "black pepper",
        "onion"
    ]

def test_analyze_dietary_restrictions():
    # Simple vegan restriction: flag eggs and cheese
    enriched_data = [
        {"ingredient": "eggs", "nutrition": {"protein": 6, "fat": 5, "carbohydrates": 1}},
        {"ingredient": "mozzarella cheese", "nutrition": {"protein": 6, "fat": 6, "carbohydrates": 1}},
        {"ingredient": "olive oil", "nutrition": {"protein": 0, "fat": 14, "carbohydrates": 0}},
        {"ingredient": "salt", "nutrition": {"protein": 0, "fat": 0, "carbohydrates": 0}},
    ]
    vegan_rules = {"exclude_ingredients": ["eggs", "mozzarella cheese"]}
    flagged = analyze_dietary_restrictions(enriched_data, vegan_rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "eggs" in flagged_names
    assert "mozzarella cheese" in flagged_names
    assert "olive oil" not in flagged_names
    assert "salt" not in flagged_names

def test_get_enhanced_swap(monkeypatch):
    # Patch dependencies for a minimal test
    def dummy_embedding_dict():
        return {"eggs": [[0.1, 0.2]], "tofu": [[0.2, 0.1]], "mozzarella cheese": [[0.3, 0.3]], "vegan cheese": [[0.3, 0.2]]}
    def dummy_knn_max(*args, **kwargs):
        class DummyKNN:
            def k_nearest_neighbors(self, emb):
                return ([0.1, 0.2], [0, 1])
        return DummyKNN()
    class DummyScaler:
        def transform(self, x): return x
    embedding_dict = dummy_embedding_dict()
    knn_max = dummy_knn_max()
    ingredient_labels = list(embedding_dict.keys())
    scaler = DummyScaler()
    restrictions = {"exclude_ingredients": ["eggs", "mozzarella cheese"]}
    swap = get_enhanced_swap("eggs", embedding_dict, knn_max, ingredient_labels, scaler, restrictions)
    assert "ranked_swaps" in swap
    assert isinstance(swap["ranked_swaps"], list)
