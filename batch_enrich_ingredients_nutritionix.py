import json
from integrate_usda_openfoodfacts import enrich_ingredient_data

if __name__ == "__main__":
    # Load ingredient list
    with open("foodBERT/foodbert_embeddings/data/used_ingredients_clean.json", "r", encoding="utf-8") as f:
        ingredient_list = json.load(f)

    # Run enrichment (uses Nutritionix as primary source)
    enriched_data = enrich_ingredient_data(ingredient_list)

    # Save output
    with open("enriched_ingredient_data_nutritionix.json", "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)

    print(f"Enriched {len(enriched_data)} ingredients using Nutritionix. Output saved to enriched_ingredient_data_nutritionix.json.")
