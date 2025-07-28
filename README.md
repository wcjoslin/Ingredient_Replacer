# Ingredient Replacer

This project provides an API and UI for robust ingredient enrichment and substitution, including nutrition, dietary category, and dietary restriction flagging, powered by foodBERT and Nutritionix data.

## Features

- **Ingredient Enrichment:**  
  - Nutrition facts (calories, protein, carbs, fat) from Nutritionix.
  - Dietary categories from foodBERT (e.g., "en:cheeses", "en:dairies").
  - Dietary restriction flagging (vegan, vegetarian, gluten-free, etc.) based on robust category matching.
  - Handles singular/plural ingredient forms and partial/missing data gracefully.

- **Ingredient Swap Suggestions:**  
  - Suggests up to 3 ranked substitutes for flagged ingredients, with confidence scores and nutrition delta.
  - Filtering and flagging logic respects user-selected dietary restrictions.

- **UI:**  
  - Paste a recipe URL, select dietary restrictions, and get enriched ingredient info and swap suggestions.

## API Endpoints

### POST `/suggestions`

Request:
```json
{
  "ingredients": ["ingredient1", "ingredient2", ...],
  "diets": ["vegan", "glutenfree", ...]  // optional
}
```

Response:
```json
{
  "suggestions": [
    {
      "original": "mozzarella cheese",
      "categories": ["en:dairies", "en:cheeses", ...],  // raw keys for logic
      "display_categories": ["Dairies", "Cheeses", ...], // user-friendly for UI
      "dietary_flags": ["Not vegan", "vegetarian-friendly"],
      "swap_suggestion": {
        "ranked_swaps": [
          {
            "substitute": "plant-based cheese",
            "score": 0.91,
            "foodbert_score": 0.93,
            "nutrition_delta": 0.05,
            "original_nutrition": {...},
            "substitute_nutrition": {...}
          }
        ]
      }
    },
    ...
  ]
}
```

- Only ingredients flagged for the selected dietary restrictions are included in the swap suggestions.
- Category and restriction matching is robust and case-insensitive.

## Enrichment Workflow

1. **Ingredient normalization:** Handles singular/plural and punctuation.
2. **Nutrition lookup:** From Nutritionix reference.
3. **Category lookup:** From foodBERT categories (raw keys and display names).
4. **Dietary restriction flagging:** Matches categories against restriction presets (case-insensitive).
5. **Swap suggestion:** For flagged ingredients, suggests up to 3 substitutes.

## Error Handling

- If nutrition or category data is missing, a clear message is included in the output.
- Partial results are returned if only some data is available.

## Manual Testing

- Paste a recipe URL in the UI, select dietary restrictions, and verify enrichment and swap suggestions.
- Test with common, rare, and unknown ingredients.

## Development

- See `Ingredient_Data_Enrichment_Implementation_Checklist.md` for step-by-step implementation and testing guidance.

---

For more details, see [API_DOCS.md](API_DOCS.md).
