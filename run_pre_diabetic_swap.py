import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "suggestic_integration")))
from foodbert_ingredient_swap import suggestic_foodbert_ingredient_swap

def main():
    with open("diet_test_recipe_selection.json", "r", encoding="utf-8") as f:
        selection = json.load(f)
    recipe_id = selection["pre_diabetic"]["id"]
    suggestic_foodbert_ingredient_swap(recipe_id, output_json_path="pre_diabetic_swap_result.json", error_log_path="pre_diabetic_swap_errors.json")

if __name__ == "__main__":
    main()
