import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from dietary_restriction_analysis import analyze_dietary_restrictions

def test_keto_restriction():
    enriched_data = [
        {"ingredient": "potato", "nutrition": {"carbohydrates": 20, "fat": 0, "protein": 2, "calories": 80}, "categories": ["en:starchy-vegetables"]},
        {"ingredient": "olive oil", "nutrition": {"carbohydrates": 0, "fat": 14, "protein": 0, "calories": 120}, "categories": ["en:oil"]},
        {"ingredient": "chicken", "nutrition": {"carbohydrates": 0, "fat": 14, "protein": 27, "calories": 239}, "categories": ["en:meats"]},
    ]
    keto_rules = {
        "max_carbohydrates_g_per_serving": 10,
        "min_fat_percent": 40,
        "exclude_categories": ["starchy vegetables", "grains", "sugar"]
    }
    flagged = analyze_dietary_restrictions(enriched_data, keto_rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "potato" in flagged_names
    assert "olive oil" not in flagged_names
    assert "chicken" not in flagged_names

def test_paleo_processed_foods():
    enriched_data = [
        {"ingredient": "chips", "nutrition": {"carbohydrates": 15, "fat": 10, "protein": 2, "calories": 150}, "categories": ["en:processed-foods"]},
        {"ingredient": "apple", "nutrition": {"carbohydrates": 12, "fat": 0, "protein": 0, "calories": 52}, "categories": ["en:fruits"]},
    ]
    paleo_rules = {
        "exclude_categories": ["processed foods", "grains", "dairy"]
    }
    flagged = analyze_dietary_restrictions(enriched_data, paleo_rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "chips" in flagged_names
    assert "apple" not in flagged_names

def test_dairy_free_and_nut_free():
    enriched_data = [
        {"ingredient": "milk", "nutrition": {"carbohydrates": 12, "fat": 8, "protein": 8, "calories": 150}, "categories": ["en:milk"]},
        {"ingredient": "almonds", "nutrition": {"carbohydrates": 6, "fat": 14, "protein": 6, "calories": 160}, "categories": ["en:nuts"]},
        {"ingredient": "rice", "nutrition": {"carbohydrates": 45, "fat": 0, "protein": 4, "calories": 200}, "categories": ["en:rices"]},
    ]
    rules = {
        "exclude_categories": ["dairy", "nut"]
    }
    flagged = analyze_dietary_restrictions(enriched_data, rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "milk" in flagged_names
    assert "almonds" in flagged_names
    assert "rice" not in flagged_names

def test_allergen_aware_flagged():
    enriched_data = [
        {"ingredient": "peanuts", "nutrition": {"carbohydrates": 6, "fat": 14, "protein": 6, "calories": 160}, "categories": ["en:nuts"], "is_flagged_allergen": True},
        {"ingredient": "rice", "nutrition": {"carbohydrates": 45, "fat": 0, "protein": 4, "calories": 200}, "categories": ["en:rices"], "is_flagged_allergen": False},
    ]
    rules = {
        "exclude_flagged_allergens": True
    }
    flagged = analyze_dietary_restrictions(enriched_data, rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "peanuts" in flagged_names
    assert "rice" not in flagged_names

def test_plant_based_exclude_animal_products():
    enriched_data = [
        {"ingredient": "chicken", "nutrition": {"carbohydrates": 0, "fat": 3, "protein": 25, "calories": 120}, "categories": ["en:animal-products"]},
        {"ingredient": "broccoli", "nutrition": {"carbohydrates": 6, "fat": 0, "protein": 2, "calories": 30}, "categories": ["en:vegetables"]},
    ]
    rules = {
        "exclude_categories": ["animal products"]
    }
    flagged = analyze_dietary_restrictions(enriched_data, rules)
    flagged_names = [item["ingredient"] for item in flagged]
    assert "chicken" in flagged_names
    assert "broccoli" not in flagged_names
