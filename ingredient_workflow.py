import json
import difflib
import re

# Load foodBERT ingredient vocabulary at module level
with open("foodBERT/foodbert_embeddings/data/used_ingredients_clean.json", "r", encoding="utf-8") as f:
    FOODBERT_INGREDIENTS = set(json.load(f))

def normalize_ingredient_string(ingredient: str) -> str:
    """
    Normalize an ingredient string by removing bullets, quantities, units, and extra text.
    Returns the cleaned string.
    """
    cleaned = ingredient
    cleaned = re.sub(r"^▢\s*", "", cleaned)
    # Remove leading fractions, numbers, and units (e.g., "¾ cup", "½ teaspoon", "¼ tsp", "¾ lb.")
    cleaned = re.sub(r"^[\d¼½¾⅓⅔⅛⅜⅝⅞\s\/\.]+(oz\.|ounce[s]?|cup[s]?|lb\.|pound[s]?|tsp\.|tbsp\.|teaspoon[s]?|tablespoon[s]?|clove[s]?|large|small|medium)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"[,].*$", "", cleaned)
    cleaned = re.sub(r"\s*see notes.*$", "", cleaned, flags=re.I)
    cleaned = cleaned.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def fuzzy_match_ingredient(cleaned: str, vocabulary=FOODBERT_INGREDIENTS, cutoff=0.6) -> str:
    """
    Fuzzy match the cleaned ingredient string to the foodBERT vocabulary.
    Returns the best match if above cutoff, else returns empty string.
    """
    matches = difflib.get_close_matches(cleaned, vocabulary, n=1, cutoff=cutoff)
    return matches[0] if matches else ""

def map_ingredients_to_foodbert(raw_ingredients: list) -> list:
    """
    For a list of raw ingredient strings, normalize and fuzzy match to foodBERT vocabulary.
    Returns a list of matched ingredient names.
    Also prints debug info for each mapping.
    """
    mapped = []
    for raw in raw_ingredients:
        norm = normalize_ingredient_string(raw)
        match = fuzzy_match_ingredient(norm)
        print(f"RAW: {raw} | NORM: {norm} | MATCH: {match}")
        if match:
            mapped.append(match)
    return mapped
