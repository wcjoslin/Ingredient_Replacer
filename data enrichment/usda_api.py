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

def get_nutrient_from_details(food_details, nutrient_name):
    nutrients = food_details.get("foodNutrients", [])
    for nutrient in nutrients:
        if nutrient.get("nutrient", {}).get("name", "").lower() == nutrient_name.lower():
            return nutrient.get("amount", 0)
    return None

def get_food_nutrition_profile(query):
    search_result = search_food(query)
    foods = search_result.get("foods", [])
    if not foods:
        return None
    
    fdc_id = foods[0].get("fdcId")
    if not fdc_id:
        return None

    food_details = get_food_nutrients(fdc_id)
    
    calories = get_nutrient_from_details(food_details, "Energy")
    protein = get_nutrient_from_details(food_details, "Protein")
    fat = get_nutrient_from_details(food_details, "Total lipid (fat)")
    carbs = get_nutrient_from_details(food_details, "Carbohydrate, by difference")

    return {
        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbohydrates": carbs
    }

def get_food_carbs(query):
    profile = get_food_nutrition_profile(query)
    return profile.get("carbohydrates") if profile else None
