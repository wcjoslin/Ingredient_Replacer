import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from suggestic_integration.suggestic_api import query_suggestic

RECIPE_QUERY = """
query SearchRecipesByIngredients($mustIngredients: [String!]!) {
  searchRecipesByIngredients(mustIngredients: $mustIngredients) {
    edges {
      node {
        
        id
      
       
          
      }
    }
  }
}
"""

def main():
    ingredient = "sugar"
    variables = {"mustIngredients": [ingredient]}
    print(f"Querying Suggestic API for ingredient: {ingredient}")
    response = query_suggestic(RECIPE_QUERY, variables)
    print("Raw API response:")
    print(response)

if __name__ == "__main__":
    main()
