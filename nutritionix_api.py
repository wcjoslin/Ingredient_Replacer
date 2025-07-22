import requests
import json
import os

NUTRITIONIX_APP_ID = "Enter ID Here"  # Replace with your actual Nutritionix API ID
NUTRITIONIX_APP_KEY = "Enter Key Here"  # Replace with your actual Nutritionix API key
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/nutrients"
CACHE_PATH = "nutritionix_cache.json"

def get_nutritionix_profile(ingredient_name):
    """
    Fetches nutrition data for a given ingredient from Nutritionix, with persistent caching.
    Returns a dict with calories, protein, fat, carbohydrates.
    """
    # Load cache
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    key = ingredient_name.lower().strip()
    if key in cache:
        return cache[key]

    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": ingredient_name
    }
    try:
        response = requests.post(NUTRITIONIX_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Nutritionix returns a list under 'foods'
        if "foods" in result and len(result["foods"]) > 0:
            food = result["foods"][0]
            profile = {
                "calories": food.get("nf_calories", 0),
                "protein": food.get("nf_protein", 0),
                "fat": food.get("nf_total_fat", 0),
                "carbohydrates": food.get("nf_total_carbohydrate", 0)
            }
            cache[key] = profile
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            return profile
        else:
            return None
    except Exception as e:
        print(f"Nutritionix API error for '{ingredient_name}': {e}")
        return None
