import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from suggestic_api import query_suggestic
import base64

RECIPE_DETAIL_QUERY = """
query getRecipe($id: ID!) {
  recipe(id: $id) {
    databaseId
    totalTime
    totalTimeInSeconds
    name
    rating
    numberOfServings
    ingredientLines
    ingredients {
      name
    }
    language
    courses
    cuisines
    source {
      siteUrl
      displayName
      recipeUrl
    }
    mainImage
    isPremium
    isFeatured
    author
    authorAvatar
    ingredientsCount
    favoritesCount
    isUserFavorite
    inUserShoppingList
    weightInGrams
    servingWeight
    isLogged
    relativeCalories {
      carbs
      fat
      protein
      fat
    }
    instructions
    nutritionalInfo {
      calories
      protein
      carbs
      fat
      sugar
      fiber
      saturatedFat
      monounsaturatedFat
      polyunsaturatedFat
      transFat
      cholesterol
      sodium
      potassium
      vitaminA
      vitaminC
      calcium
      iron
      netcarbs
    }
  }
}
"""

def main():
    with open("diet_test_recipe_selection.json", "r", encoding="utf-8") as f:
        selection = json.load(f)
    results = {}
    for key, recipe in selection.items():
        # Try base64-encoded id first
        variables = {"id": recipe["id"]}
        response = query_suggestic(RECIPE_DETAIL_QUERY, variables)
        data = response.get("data", {}).get("recipe", {})
        if not data:
            # Try raw databaseId if available
            try:
                decoded = base64.b64decode(recipe["id"]).decode()
                # databaseId is after the last colon
                dbid = decoded.split(":")[-1]
                variables = {"id": dbid}
                response = query_suggestic(RECIPE_DETAIL_QUERY, variables)
                data = response.get("data", {}).get("recipe", {})
            except Exception:
                pass
        results[key] = data
    with open("diet_test_recipe_details.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
