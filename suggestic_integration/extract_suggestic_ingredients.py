import json
from suggestic_api import query_suggestic

COMMON_INGREDIENTS = [
    "chicken", "beef", "pork", "fish", "egg", "milk", "cheese", "rice", "beans", "tomato",
    "potato", "onion", "garlic", "carrot", "pepper", "lettuce", "spinach", "broccoli", "apple", "banana"
]

def fetch_ingredients():
    unique_ingredients = set()
    for keyword in COMMON_INGREDIENTS:
        query = f'''
        {{
          recipeSearch(query: "{keyword}") {{
            edges {{
              node {{
                ingredients {{
                  name
                }}
              }}
            }}
          }}
        }}
        '''
        result = query_suggestic(query)
        recipes = result.get("data", {}).get("recipeSearch", {}).get("edges", [])
        for recipe in recipes:
            for ing in recipe["node"].get("ingredients", []):
                unique_ingredients.add(ing["name"].strip().lower())
    return sorted(unique_ingredients)

def save_ingredients_to_json(ingredients, filename="suggestic_ingredients.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ingredients = fetch_ingredients()
    save_ingredients_to_json(ingredients)
    print(f"Extracted {len(ingredients)} unique ingredients to suggestic_ingredients.json")
