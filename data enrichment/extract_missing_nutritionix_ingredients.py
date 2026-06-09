import json

with open("enriched_ingredient_data_nutritionix.json", "r", encoding="utf-8") as f:
    data = json.load(f)

missing = []
for entry in data:
    profile = entry["nutritionix_nutrition_profile"]
    if any(v == "TBD" for v in profile.values()):
        missing.append(entry["ingredient"])

with open("outputs/missing_nutritionix_ingredients.json", "w", encoding="utf-8") as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)

print(f"Found {len(missing)} ingredients with missing nutrition data. Output saved to missing_nutritionix_ingredients.json.")
