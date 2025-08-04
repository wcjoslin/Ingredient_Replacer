import json
import re

# Load merged ingredient categories and mapping
with open("foodbert_ingredient_categories_merged.json", "r", encoding="utf-8") as f:
    ingredient_cats = json.load(f)
with open("category_mapping_and_primary_tags.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

primary_map = mapping["primary_category_map"]

# Priority order: functional/processed > staple > broad
priority_order = [
    "pasta", "bread", "rice", "flour", "bean", "cheese", "milk", "egg", "meat", "fish", "oil", "sweetener", "nut", "seed", "vegetable", "fruit", "spice", "sauce"
]

# Manual overrides for common problematic ingredients
manual_overrides = {
    # Fruits
    "apple": "fruit", "apples": "fruit", "banana": "fruit", "bananas": "fruit",
    "lemon": "fruit", "lime": "fruit", "orange": "fruit", "oranges": "fruit",
    "grapes": "fruit", "raisins": "fruit", "plums": "fruit", "cherries": "fruit",
    "blueberries": "fruit", "strawberries": "fruit", "blackberries": "fruit", "raspberries": "fruit",
    "kiwi": "fruit", "mango": "fruit", "pineapple": "fruit", "pear": "fruit", "pears": "fruit",
    "apricot": "fruit", "apricots": "fruit", "fig": "fruit", "figs": "fruit", "date": "fruit", "dates": "fruit",
    # Flours
    "coconut flour": "flour", "almond flour": "flour", "oat flour": "flour", "rice flour": "flour",
    "potato flour": "flour", "corn flour": "flour", "cornstarch": "flour", "arrowroot powder": "flour",
    # Nuts & Seeds
    "pecan": "nut", "pecans": "nut", "walnuts": "nut", "hazelnuts": "nut", "macadamia nuts": "nut",
    "pistachios": "nut", "cashews": "nut", "peanuts": "nut", "peanut butter": "nut", "almond butter": "nut",
    "chia seeds": "seed", "flax seed": "seed", "flax seeds": "seed", "pumpkin seeds": "seed",
    "water chestnut": "nut",
    # Oils
    "coconut oil": "oil", "flaxseed oil": "oil", "olive oil": "oil", "canola oil": "oil",
    "vegetable oil": "oil", "sunflower oil": "oil",
    # Milks & Creams
    "coconut milk": "milk", "coconut cream": "milk", "almond milk": "milk", "cashew milk": "milk",
    "soy milk": "milk",
    # Sweeteners
    "coconut sugar": "sweetener",
    # Vegetables
    "cabbage": "vegetable", "chives": "vegetable", "green bell pepper": "vegetable", "green onion": "vegetable",
    "leeks": "vegetable", "lentils": "vegetable", "peas": "vegetable", "pickles": "vegetable", "potato": "vegetable",
    "pumpkin": "vegetable", "red onion": "vegetable", "red pepper": "vegetable", "red potatoes": "vegetable",
    "romaine lettuce": "vegetable", "russet potato": "vegetable", "serrano": "vegetable", "squash": "vegetable",
    "yellow onion": "vegetable", "vegetables": "vegetable",
    "lettuce": "vegetable", "spinach": "vegetable", "zucchini": "vegetable", "carrots": "vegetable",
    "broccoli": "vegetable", "cauliflower": "vegetable", "bell peppers": "vegetable", "tomato": "vegetable",
    "tomatoes": "vegetable", "onion": "vegetable", "onions": "vegetable", "garlic": "vegetable", "ginger": "vegetable",
    # Spices
    "chili": "spice", "chili pepper": "spice", "cilantro": "spice", "cloves": "spice", "coriander": "spice",
    "cumin": "spice", "cumin seed": "spice", "onion powder": "spice", "onion salt": "spice", "paprika": "spice",
    "smoked paprika": "spice", "nutmeg": "spice", "black pepper": "spice", "thyme": "spice",
    # Meats
    "beef": "meat", "pork": "meat", "chicken": "meat", "chorizo": "meat", "turkey": "meat"
}

# Keyword-based fallback
keyword_map = [
    (r"\bflour\b", "flour"),
    (r"\bbread\b", "bread"),
    (r"\bpasta\b", "pasta"),
    (r"\brice\b", "rice"),
    (r"\bbean\b", "bean"),
    (r"\bcheese\b", "cheese"),
    (r"\bmilk\b", "milk"),
    (r"\begg?\b", "egg"),
    (r"\bmeat\b", "meat"),
    (r"\bfish\b", "fish"),
    (r"\boil\b", "oil"),
    (r"\bseed\b", "seed"),
    (r"\bnut\b", "nut"),
    (r"\bfruit\b", "fruit"),
    (r"\bvegetable\b", "vegetable"),
    (r"\bspice\b", "spice"),
    (r"\bsauce\b", "sauce"),
    (r"\bsweetener\b", "sweetener"),
    (r"\bsugar\b", "sweetener"),
    (r"\bsyrup\b", "sweetener")
]

def get_primary_category(ingredient, categories):
    # 1. Manual override
    if ingredient in manual_overrides:
        return manual_overrides[ingredient]
    # 2. Priority mapping
    for primary in priority_order:
        cat_list = primary_map.get(primary, [])
        if any(cat in categories for cat in cat_list):
            return primary
    # 3. Keyword fallback
    for pattern, primary in keyword_map:
        if re.search(pattern, ingredient):
            return primary
    # 4. Fallback: match any primary (unordered)
    for primary, cat_list in primary_map.items():
        if any(cat in categories for cat in cat_list):
            return primary
    return "other"

primary_categories = {}
for ingredient, cats in ingredient_cats.items():
    primary = get_primary_category(ingredient, cats)
    primary_categories[ingredient] = primary

with open("ingredient_primary_categories.json", "w", encoding="utf-8") as f:
    json.dump(primary_categories, f, ensure_ascii=False, indent=2)

print("Assigned primary categories to all ingredients (hybrid approach + user feedback). Output: ingredient_primary_categories.json")
