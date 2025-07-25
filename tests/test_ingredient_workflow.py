# Python

import json
import unittest
from unittest.mock import patch, mock_open

class TestIngredientWorkflowFiltering(unittest.TestCase):
    def setUp(self):
        # Example flagged ingredients
        self.flagged_ingredients = [
            {"ingredient": "beef", "nutrition": {"carbohydrates": 0}},
            {"ingredient": "banana", "nutrition": {"carbohydrates": 23}},
            {"ingredient": "black pepper", "nutrition": {"carbohydrates": 1}},
            {"ingredient": "almond flour", "nutrition": {"carbohydrates": 10}},
            {"ingredient": "coconut oil", "nutrition": {"carbohydrates": 0}},
            {"ingredient": "unknown ingredient", "nutrition": {"carbohydrates": 5}},
        ]
        # Example primary categories
        self.primary_categories = {
            "beef": "meat",
            "banana": "fruit",
            "black pepper": "spice",
            "almond flour": "flour",
            "coconut oil": "oil",
        }
        # Example common spices
        self.common_spices = {"black pepper"}

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "beef": "meat",
        "banana": "fruit",
        "black pepper": "spice",
        "almond flour": "flour",
        "coconut oil": "oil"
    }))
    def test_filtering_logic(self, mock_file):
        # Simulate filtering logic from ingredient_workflow.py
        filtered_flagged = []
        for item in self.flagged_ingredients:
            name = item["ingredient"].lower().strip()
            if name in self.common_spices:
                continue
            nutrition = item.get("nutrition", {})
            if nutrition and nutrition.get("carbohydrates", 0) <= 10:
                continue
            target_category = self.primary_categories.get(name)
            if not target_category:
                continue
            if self.primary_categories.get(name) != target_category:
                continue
            filtered_flagged.append(item)
        # Only banana should remain (carbs > 10, not a spice, has category)
        self.assertEqual(len(filtered_flagged), 1)
        self.assertEqual(filtered_flagged[0]["ingredient"], "banana")

    def test_missing_category(self):
        # Ingredient not in primary_categories should be skipped
        filtered_flagged = []
        for item in self.flagged_ingredients:
            name = item["ingredient"].lower().strip()
            target_category = self.primary_categories.get(name)
            if not target_category:
                continue
            filtered_flagged.append(item)
        # "unknown ingredient" should be excluded
        self.assertNotIn("unknown ingredient", [i["ingredient"] for i in filtered_flagged])

if __name__ == "__main__":
    unittest.main()
