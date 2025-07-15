import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
from suggestic_integration.suggestic_api import query_suggestic

RECIPE_QUERY = """
query SearchRecipesByIngredients($mustIngredients: [String!]!) {
  searchRecipesByIngredients(mustIngredients: $mustIngredients) {
    edges {
      node {
        name
        id
        ingredients {
          name
        }
        instructions
      }
    }
  }
}
"""

# Load ingredients below threshold
with open("tests/ingredients_below_40_sentences.json", "r", encoding="utf-8") as f:
    ingredients = list(json.load(f).keys())

def get_all_instructions_for_ingredient(ingredient, max_retries=5, max_recipes=50):
    all_instructions = []
    recipe_log = []
    recipe_ids = set()
    retries = 0
    backoff = 5
    while retries < max_retries:
        variables = {
            "mustIngredients": [ingredient]
        }
        try:
            print(f"DEBUG: Querying API for ingredient: {ingredient} with variables: {variables}")
            data = query_suggestic(RECIPE_QUERY, variables)
            print(f"DEBUG: API response for {ingredient}: {data}")
            edges = data.get("data", {}).get("searchRecipesByIngredients", {}).get("edges", [])
            if not edges:
                print(f"DEBUG: No more edges for {ingredient}.")
                break
            for edge in edges[:max_recipes]:
                node = edge.get("node", {})
                recipe_id = node.get("id")
                if recipe_id in recipe_ids:
                    continue  # Skip duplicates
                recipe_ids.add(recipe_id)
                recipe_log.append({
                    "id": recipe_id,
                    "name": node.get("name"),
                    "ingredients": [ing.get("name") for ing in node.get("ingredients", [])],
                    "instructions": node.get("instructions")
                })
                # Add all instructions (list of strings)
                if node.get("instructions"):
                    for instr in node.get("instructions"):
                        if instr:
                            all_instructions.append(instr.strip())
                if len(recipe_ids) >= max_recipes:
                    print(f"DEBUG: Reached max_recipes ({max_recipes}) for {ingredient}.")
                    break
            break  # Only one API call needed, no pagination
        except Exception as e:
            print(f"Error querying '{ingredient}': {e}")
            print(f"Backing off for {backoff} seconds due to error.")
            time.sleep(backoff)
            retries += 1
            backoff = min(backoff * 2, 300)  # Exponential backoff, max 5 minutes
    return all_instructions, recipe_log

def main():
    all_instructions_dict = {}
    recipe_logs = {}
    skipped_ingredients = []
    for idx, ingredient in enumerate(ingredients):
        print(f"Processing {idx+1}/{len(ingredients)}: {ingredient}")
        instructions, recipes = get_all_instructions_for_ingredient(ingredient)
        if not instructions:
            print(f"WARNING: No recipes found for ingredient '{ingredient}'. Skipping.")
            skipped_ingredients.append(ingredient)
            continue
        all_instructions_dict[ingredient] = instructions
        recipe_logs[ingredient] = recipes
        # Save progress every 10 ingredients
        if (idx + 1) % 10 == 0:
            with open("all_ingredient_instructions.json", "w", encoding="utf-8") as f:
                json.dump(all_instructions_dict, f, ensure_ascii=False, indent=2)
            with open("expanded_ingredient_recipe_logs.json", "w", encoding="utf-8") as f:
                json.dump(recipe_logs, f, ensure_ascii=False, indent=2)
            with open("skipped_ingredients.json", "w", encoding="utf-8") as f:
                json.dump(skipped_ingredients, f, ensure_ascii=False, indent=2)
    # Final save
    with open("all_ingredient_instructions.json", "w", encoding="utf-8") as f:
        json.dump(all_instructions_dict, f, ensure_ascii=False, indent=2)
    with open("expanded_ingredient_recipe_logs.json", "w", encoding="utf-8") as f:
        json.dump(recipe_logs, f, ensure_ascii=False, indent=2)
    with open("skipped_ingredients.json", "w", encoding="utf-8") as f:
        json.dump(skipped_ingredients, f, ensure_ascii=False, indent=2)
    print("Saved all instructions, recipe logs, and skipped ingredients.")

if __name__ == "__main__":
    main()
