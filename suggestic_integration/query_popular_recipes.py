import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from suggestic_api import query_suggestic

POPULAR_RECIPES_QUERY = """
{
  popularRecipes {
    edges {
      node {
        id
        name
      }
    }
  }
}
"""

def main():
    response = query_suggestic(POPULAR_RECIPES_QUERY)
    recipes = []
    edges = response.get("data", {}).get("popularRecipes", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        recipes.append({
            "id": node.get("id"),
            "name": node.get("name")
        })
    with open("outputs/popular_recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
