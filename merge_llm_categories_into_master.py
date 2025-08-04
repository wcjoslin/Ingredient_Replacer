import json

# Load main categories file
with open("foodbert_ingredient_categories.json", "r", encoding="utf-8") as f:
    main_cats = json.load(f)

# Load LLM-generated categories
with open("foodbert_ingredient_categories_llm.json", "r", encoding="utf-8") as f:
    llm_cats = json.load(f)

# Merge: for each LLM entry, if the main file has an empty list, fill it in
for ingredient, llm_labels in llm_cats.items():
    if ingredient in main_cats and (not main_cats[ingredient] or main_cats[ingredient] == ["en:undefined"]):
        main_cats[ingredient] = llm_labels

# Save merged result
with open("foodbert_ingredient_categories_merged.json", "w", encoding="utf-8") as f:
    json.dump(main_cats, f, ensure_ascii=False, indent=2)

print("Merged LLM categories into master ingredient categories file: foodbert_ingredient_categories_merged.json")
