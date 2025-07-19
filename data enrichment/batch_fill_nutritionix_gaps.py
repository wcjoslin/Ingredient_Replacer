import json
import time
from nutritionix_api import get_nutritionix_profile

MAX_API_CALLS = 200

with open("missing_nutritionix_ingredients.json", "r", encoding="utf-8") as f:
    missing = json.load(f)

with open("enriched_ingredient_data_nutritionix.json", "r", encoding="utf-8") as f:
    enriched = json.load(f)

calls_made = 0
for ingredient in missing:
    if calls_made >= MAX_API_CALLS:
        print(f"Reached {MAX_API_CALLS} API calls. Stopping for today.")
        break
    try:
        nutrition = get_nutritionix_profile(ingredient)
        # Update the enriched data
        for entry in enriched:
            if entry["ingredient"] == ingredient:
                entry["nutritionix_nutrition_profile"] = nutrition
                break
        calls_made += 1
        time.sleep(0.5)  # Optional: avoid hitting rate limits
        print(f"Filled: {ingredient}")
    except Exception as e:
        print(f"Failed to fetch {ingredient}: {e}")

with open("enriched_ingredient_data_nutritionix.json", "w", encoding="utf-8") as f:
    json.dump(enriched, f, ensure_ascii=False, indent=2)

print(f"Filled {calls_made} ingredients. Updated enriched_ingredient_data_nutritionix.json.")
