import requests
from config import USDA_API_KEY, USDA_API_URL

def search_food(query, page_size=5):
    url = f"{USDA_API_URL}/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": query,
        "pageSize": page_size
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_food_nutrients(fdc_id):
    url = f"{USDA_API_URL}/food/{fdc_id}"
    params = {
        "api_key": USDA_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_carbs_from_nutrients(nutrients):
    for nutrient in nutrients:
        if nutrient.get("name", "").lower() == "carbohydrate, by difference":
            return nutrient.get("amount", 0)
    return None

def get_food_carbs(query):
    search_result = search_food(query)
    foods = search_result.get("foods", [])
    if not foods:
        return None
    fdc_id = foods[0].get("fdcId")
    food_details = get_food_nutrients(fdc_id)
    nutrients = food_details.get("foodNutrients", [])
    carbs = get_carbs_from_nutrients(nutrients)
    return carbs
