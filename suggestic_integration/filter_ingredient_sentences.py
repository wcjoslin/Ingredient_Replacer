import json
import re

INPUT_FILE = "all_ingredient_instructions.json"
OUTPUT_FILE = "outputs/filtered_ingredient_sentences.json"
SKIPPED_FILE = "outputs/filtered_skipped_ingredients.json"

def normalize(text):
    return re.sub(r"[^a-zA-Z0-9 ]", "", text).lower()

def sentence_mentions_ingredient(sentence, ingredient):
    norm_sentence = normalize(sentence)
    norm_ingredient = normalize(ingredient)
    return norm_ingredient in norm_sentence

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        ingredient_sentences = json.load(f)

    filtered_sentences = {}
    skipped_ingredients = []

    for ingredient, sentences in ingredient_sentences.items():
        filtered = [s for s in sentences if sentence_mentions_ingredient(s, ingredient)]
        if filtered:
            filtered_sentences[ingredient] = filtered
        else:
            skipped_ingredients.append(ingredient)
        print(f"{ingredient}: {len(filtered)} sentences kept out of {len(sentences)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered_sentences, f, ensure_ascii=False, indent=2)

    with open(SKIPPED_FILE, "w", encoding="utf-8") as f:
        json.dump(skipped_ingredients, f, ensure_ascii=False, indent=2)

    print(f"Filtered sentences saved to {OUTPUT_FILE}")
    print(f"Skipped ingredients saved to {SKIPPED_FILE}")

if __name__ == "__main__":
    main()
