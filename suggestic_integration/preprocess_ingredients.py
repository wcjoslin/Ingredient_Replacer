import json

def load_ingredients(filename="suggestic_ingredients.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    # If the file is a list, return as is; if it's a dict, extract the list
    if isinstance(data, list):
        return data
    # If it's a dict with a "data" key, try to extract ingredients
    if "data" in data:
        return data["data"].get("ingredients", [])
    return []

def normalize_ingredients(ingredients):
    normalized = set()
    for ing in ingredients:
        if isinstance(ing, str):
            name = ing.strip().lower()
        elif isinstance(ing, dict) and "name" in ing:
            name = ing["name"].strip().lower()
        else:
            continue
        if name:
            normalized.add(name)
    return sorted(normalized)

def save_normalized_ingredients(ingredients, filename="foodbert_ready_ingredients.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    ingredients = load_ingredients()
    normalized = normalize_ingredients(ingredients)
    save_normalized_ingredients(normalized)
    print(f"Saved {len(normalized)} normalized ingredients to foodbert_ready_ingredients.json")
