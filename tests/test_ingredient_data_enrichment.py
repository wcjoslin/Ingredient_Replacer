import pytest
import sys
import os

# Ensure import from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingredient_data_enrichment import (
    enrich_ingredient,
    normalize_ingredient_name,
)

# Mock data for testing
MOCK_NUTRITION = {
    "egg": {"calories": 70, "protein": 6, "carbs": 1, "fat": 5},
    "milk": {"calories": 100, "protein": 8, "carbs": 12, "fat": 2.5},
}
MOCK_CATEGORIES = {
    "egg": ["animal_product", "protein"],
    "milk": ["animal_product", "dairy"],
    "flour": ["grain", "gluten"],
}
MOCK_DIETARY_PRESETS = {
    "vegan": {"exclude_categories": ["animal_product", "dairy"]},
    "gluten_free": {"exclude_categories": ["gluten"]},
}

def test_normalize_ingredient_name():
    assert normalize_ingredient_name("Egg") == "egg"
    assert normalize_ingredient_name("  MILK  ") == "milk"
    assert normalize_ingredient_name("Flour!") == "flour"
    assert normalize_ingredient_name("Eggs, large") == "eggs large"

def test_enrich_ingredient_full_data():
    bullets = enrich_ingredient(
        "Egg", MOCK_NUTRITION, MOCK_CATEGORIES, MOCK_DIETARY_PRESETS
    )
    assert "Calories: 70" in bullets
    assert "Protein: 6" in bullets
    assert "Category: animal_product" in bullets
    assert "Not vegan" in bullets
    assert "gluten_free-friendly" in bullets

def test_enrich_ingredient_partial_data():
    bullets = enrich_ingredient(
        "Flour", MOCK_NUTRITION, MOCK_CATEGORIES, MOCK_DIETARY_PRESETS
    )
    assert "Category: grain" in bullets
    assert "Not gluten_free" in bullets
    assert "vegan-friendly" in bullets
    assert not any("Calories" in b for b in bullets)

def test_enrich_ingredient_missing_data():
    bullets = enrich_ingredient(
        "Unknown Ingredient", MOCK_NUTRITION, MOCK_CATEGORIES, MOCK_DIETARY_PRESETS
    )
    assert any("Nutritional Information for Unknown Ingredient is incomplete" in b for b in bullets)

def test_enrich_ingredient_multiple_flags():
    # Add a mock ingredient that matches multiple restrictions
    nutrition = {"calories": 200, "protein": 10, "carbs": 30, "fat": 5}
    categories = ["animal_product", "gluten"]
    bullets = enrich_ingredient(
        "Mock Ingredient",
        {"mock ingredient": nutrition},
        {"mock ingredient": categories},
        MOCK_DIETARY_PRESETS,
    )
    assert "Not vegan" in bullets
    assert "Not gluten_free" in bullets
    assert "Calories: 200" in bullets
    assert "Category: animal_product" in bullets
    assert "Category: gluten" in bullets

if __name__ == "__main__":
    pytest.main([__file__])
