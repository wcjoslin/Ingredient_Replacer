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

class TestMultiIngredientSuggestionRanking(unittest.TestCase):
    def test_ranked_swaps_structure(self):
        # Simulate API output for multi-ingredient suggestion
        api_response = {
            "swap_suggestion": {
                "ranked_swaps": [
                    {"substitute": "greek yogurt", "score": 0.92},
                    {"substitute": "cottage cheese", "score": 0.85},
                    {"substitute": "quark", "score": 0.80}
                ]
            }
        }
        ranked = api_response["swap_suggestion"]["ranked_swaps"]
        self.assertTrue(isinstance(ranked, list))
        self.assertLessEqual(len(ranked), 3)
        self.assertEqual(ranked[0]["substitute"], "greek yogurt")
        self.assertGreater(ranked[0]["score"], ranked[1]["score"])
        self.assertGreater(ranked[1]["score"], ranked[2]["score"])

    def test_ranked_swaps_edge_cases(self):
        # 0 results
        api_response = {"swap_suggestion": {"ranked_swaps": []}}
        self.assertEqual(len(api_response["swap_suggestion"]["ranked_swaps"]), 0)
        # 1 result
        api_response = {"swap_suggestion": {"ranked_swaps": [{"substitute": "greek yogurt", "score": 0.92}]}}
        self.assertEqual(len(api_response["swap_suggestion"]["ranked_swaps"]), 1)
        # 2 results
        api_response = {"swap_suggestion": {"ranked_swaps": [
            {"substitute": "greek yogurt", "score": 0.92},
            {"substitute": "cottage cheese", "score": 0.85}
        ]}}
        self.assertEqual(len(api_response["swap_suggestion"]["ranked_swaps"]), 2)

if __name__ == "__main__":
    unittest.main()
