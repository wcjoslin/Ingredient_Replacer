# Ingredient Replacer API Documentation

## Overview

This API provides robust ingredient enrichment and substitution, including:
- Nutrition facts (from Nutritionix)
- Dietary categories (from foodBERT)
- Dietary restriction flagging (vegan, vegetarian, gluten-free, etc.)
- Ranked ingredient swap suggestions

## Endpoints

### GET `/diet_rules`

**Request:**  
No parameters.

**Response:**
```json
{
  "diets": [
    {
      "id": "vegan",
      "name": "Vegan",
      "description": "Veganism excludes all animal products, including meat, dairy, eggs, and honey. The diet is based on plant foods such as vegetables, grains, nuts, seeds, legumes, and fruits.",
      "category_restrictions": [
        {"text": "No dairy", "full": "No dairy"},
        {"text": "No meats", "full": "No meats"}
      ],
      "macronutrient_restrictions": [
        {"text": "Max 10g carbs per ingredient", "full": "Max 10g carbs per ingredient"}
      ]
    }
  ]
}
```
- Returns all available diet rules, including description, category restrictions, and macronutrient restrictions.
- Long rules are truncated in `text` with the full rule in `full` for tooltips.

### POST `/enrich_ingredients`

**Request:**
```json
{
  "ingredients": ["ingredient1", "ingredient2", ...]
}
```

**Response:**
```json
{
  "ingredients": [
    {
      "ingredient": "mozzarella cheese",
      "nutrition_facts": {
        "calories": 85,
        "protein": 6.3,
        "carbs": 0.6,
        "fat": 6.3
      },
      "categories": ["en:dairies", "en:cheeses", ...],
      "swap_rationales": ["Category: Vegan excluded"],
      "dietary_change_description": "Ingredient does not comply with selected diet(s): Category: Vegan excluded",
      "bullet_points": [
        "Calories: 85",
        "Protein: 6.3",
        "Carbs: 0.6",
        "Fat: 6.3",
        "Category: en:dairies",
        "Flagged: Category: Vegan excluded"
      ]
    }
  ]
}
```
- Returns enrichment for each ingredient, including nutrition, categories, all swap rationales, and dietary change description.
- `bullet_points` is for display; use `swap_rationales` and `dietary_change_description` for logic and tooltips.

### POST `/suggestions`

**Request:**
```json
{
  "ingredients": ["ingredient1", "ingredient2", ...],
  "diets": ["vegan", "glutenfree", ...]  // optional
}
```

- `ingredients`: List of ingredient names (cleaned, e.g., from recipe parsing)
- `diets`: Array of dietary restriction keys (see below for options)

**Response:**
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

## Dietary Restriction Keys

Supported values for the `diets` array (case-insensitive):
- `"vegan"`
- `"vegetarian"`
- `"glutenfree"`
- `"dairyfree"`
- `"lowcarb"`
- `"paleo"`
- `"keto"`
- (See `dietary_restriction_presets.json` for full list and logic.)

## Enrichment & Swap Workflow

1. **Ingredient normalization:** Handles singular/plural and punctuation.
2. **Nutrition lookup:** From Nutritionix reference.
3. **Category lookup:** From foodBERT categories (raw keys and display names).
4. **Dietary restriction flagging:** Matches categories against restriction presets (case-insensitive).
5. **Swap suggestion:** For flagged ingredients, suggests up to 3 substitutes.

## Error Handling

- If nutrition or category data is missing, a clear message is included in the output.
- Partial results are returned if only some data is available.

## Example Usage

**Request:**
```json
{
  "ingredients": ["mozzarella cheese", "lasagna noodles"],
  "diets": ["vegan"]
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "original": "mozzarella cheese",
      "categories": ["en:dairies", "en:cheeses"],
      "display_categories": ["Dairies", "Cheeses"],
      "dietary_flags": ["Not vegan", "vegetarian-friendly"],
      "swap_suggestion": {
        "ranked_swaps": [
          {
            "substitute": "plant-based cheese",
            "score": 0.91,
            "foodbert_score": 0.93,
            "nutrition_delta": 0.05,
            "original_nutrition": {"calories": 85, "protein": 6.3, "carbohydrates": 0.6, "fat": 6.3},
            "substitute_nutrition": {"calories": 70, "protein": 2.0, "carbohydrates": 1.0, "fat": 4.0}
          }
        ]
      }
    }
  ]
}
```

## Notes

- The API is designed for synchronous use during recipe upload or ingredient analysis.
- For more details on the enrichment and swap logic, see [README.md](README.md).

---
