import json
from pathlib import Path

def load_ingredients(ingredient_path):
    with open(ingredient_path, "r", encoding="utf-8") as f:
        return [i.strip().lower() for i in json.load(f)]

def load_sentences(*paths):
    sentences = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            sentences.extend([line.strip().lower() for line in f if line.strip()])
    return sentences

def find_missing_ingredients(ingredients, sentences):
    missing = []
    for ingredient in ingredients:
        found = any(ingredient in sentence for sentence in sentences)
        if not found:
            missing.append(ingredient)
    return missing

def generate_example_sentences(ingredient, n=3):
    templates = [
        f"Add {ingredient} to the pan.",
        f"Stir in the {ingredient} until combined.",
        f"Drizzle {ingredient} over the dish."
    ]
    return templates[:n]

def main():
    ingredient_path = "foodBERT/foodbert_embeddings/data/used_ingredients_clean.json"
    train_path = "foodBERT/foodbert/data/train_instructions.txt"
    test_path = "foodBERT/foodbert/data/test_instructions.txt"

    ingredients = load_ingredients(ingredient_path)
    sentences = load_sentences(train_path, test_path)
    missing = find_missing_ingredients(ingredients, sentences)

    print(f"Total ingredients: {len(ingredients)}")
    print(f"Ingredients missing from instructions: {len(missing)}")
    if missing:
        print("\nMissing ingredients:")
        for ingredient in missing:
            print(ingredient)
        print("\nExample sentences for missing ingredients:")
        for ingredient in missing:
            for sentence in generate_example_sentences(ingredient):
                print(sentence)
    else:
        print("All ingredients are covered in the instruction files.")

if __name__ == "__main__":
    main()
