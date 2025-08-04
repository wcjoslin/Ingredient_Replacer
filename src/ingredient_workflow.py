import json
import difflib
import re
import spacy

# Load spaCy English model at module level
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    NLP = None  # spaCy model not loaded

# Load foodBERT ingredient vocabulary at module level
with open("foodBERT/foodbert_embeddings/data/used_ingredients_clean.json", "r", encoding="utf-8") as f:
    FOODBERT_INGREDIENTS = set(json.load(f))

def normalize_ingredient_string(ingredient: str) -> str:
    """
    Normalize an ingredient string by removing bullets, quantities, units, preparation instructions, and extra text.
    Returns the cleaned string.
    """
    cleaned = ingredient
    cleaned = re.sub(r"^▢\s*", "", cleaned)
    # Remove leading fractions, numbers, and units (e.g., "¾ cup", "½ teaspoon", "¼ tsp", "¾ lb.")
    cleaned = re.sub(
        r"^[\d¼½¾⅓⅔⅛⅜⅝⅞\s\/\.]+(oz\.|ounce[s]?|cup[s]?|lb\.|pound[s]?|tsp\.|tbsp\.|teaspoon[s]?|tablespoon[s]?|clove[s]?|pinch|dash|can[s]?|package[s]?|slice[s]?|piece[s]?|bunch|stick[s]?|large|small|medium)?\s*",
        "",
        cleaned,
        flags=re.I,
    )
    # Remove common preparation instructions and adjectives
    cleaned = re.sub(
        r"\b(chopped|diced|minced|sliced|peeled|grated|shredded|halved|quartered|seeded|cooked|drained|rinsed|fresh|frozen|optional|to taste|thinly|thickly|crushed|ground|julienned|cubed|coarsely|finely|softened|melted|beaten|whipped|blanched|steamed|roasted|baked|boiled|fried|raw|prepared|cut into pieces|cut|cut up|split|separated|divided|reserved|warm|cold|room temperature)\b",
        "",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(r"[,].*$", "", cleaned)
    cleaned = re.sub(r"\s*see notes.*$", "", cleaned, flags=re.I)
    cleaned = cleaned.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def extract_core_ingredient_spacy(text: str) -> str:
    """
    Use spaCy to extract the main noun or noun phrase from the normalized ingredient string.
    Falls back to input if spaCy is unavailable or no noun found.
    """
    if NLP is None:
        return text
    doc = NLP(text)
    # Find the longest noun chunk or noun token
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    if noun_chunks:
        return max(noun_chunks, key=len)
    # Fallback: find first noun token
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    if nouns:
        return nouns[0]
    return text

def fuzzy_match_ingredient(cleaned: str, vocabulary=FOODBERT_INGREDIENTS, cutoff=0.6) -> str:
    """
    Fuzzy match the cleaned ingredient string to the foodBERT vocabulary.
    Returns the best match if above cutoff, else returns empty string.
    """
    matches = difflib.get_close_matches(cleaned, vocabulary, n=1, cutoff=cutoff)
    return matches[0] if matches else ""

def map_ingredients_to_foodbert(raw_ingredients: list) -> list:
    """
    For a list of raw ingredient strings, normalize, extract core noun phrase, and fuzzy match to foodBERT vocabulary.
    Returns a list of matched ingredient names.
    Also prints debug info for each mapping.
    """
    mapped = []
    for raw in raw_ingredients:
        norm = normalize_ingredient_string(raw)
        core = extract_core_ingredient_spacy(norm)
        match = fuzzy_match_ingredient(core)
        print(f"RAW: {raw} | NORM: {norm} | CORE: {core} | MATCH: {match}")
        if match:
            mapped.append(match)
    return mapped
