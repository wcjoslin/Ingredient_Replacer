import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recipe_nutrition_label_workflow import (
    parse_recipe,
    load_nutrition_data,
    sum_recipe_nutrition,
    generate_nutrition_label_image,
)

def test_parse_recipe():
    recipe = {
        "ingredients": [
            {"name": "all purpose flour", "amount": "2 cups"},
            "egg"
        ],
        "servings": 2
    }
    ingr_list, servings = parse_recipe(recipe)
    assert ingr_list == ["all purpose flour", "egg"]
    assert servings == 2

def test_sum_recipe_nutrition():
    nutrition_data = {
        "all purpose flour": {"calories": 100, "protein": 3, "fat": 0.3, "carbohydrates": 22},
        "egg": {"calories": 70, "protein": 6, "fat": 5, "carbohydrates": 1}
    }
    ingr_list = ["all purpose flour", "egg"]
    servings = 2
    summary = sum_recipe_nutrition(ingr_list, nutrition_data, servings)
    assert summary["total"]["calories"] == 170
    assert summary["per_serving"]["calories"] == 85

def test_generate_nutrition_label_image(tmp_path):
    nutrition_data = {
        "all purpose flour": {"calories": 100, "protein": 3, "fat": 0.3, "carbohydrates": 22},
        "egg": {"calories": 70, "protein": 6, "fat": 5, "carbohydrates": 1}
    }
    ingr_list = ["all purpose flour", "egg"]
    servings = 2
    summary = sum_recipe_nutrition(ingr_list, nutrition_data, servings)
    output_path = tmp_path / "test_label.png"
    generate_nutrition_label_image(summary, ingr_list, nutrition_data, str(output_path))
    assert os.path.exists(output_path)
