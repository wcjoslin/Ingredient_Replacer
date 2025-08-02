# Multi-Ingredient Suggestion API Documentation

## Overview
This API provides up to 3 ranked ingredient substitutes for each input ingredient, including confidence scores and nutrition details.

## Response Format

Each ingredient swap suggestion returns:
```json
{
  "ingredient": "original_ingredient_name",
  "rationale": "reason for swap",
  "swap_suggestion": {
    "ranked_swaps": [
      {
        "substitute": "substitute_ingredient_name",
        "score": float,
        "foodbert_score": float,
        "nutrition_delta": float,
        "original_nutrition": {...},
        "substitute_nutrition": {...}
      },
      ...
    ]
  }
}
```

- `ranked_swaps`: Array of up to 3 substitutes, sorted by descending score.
- `score`: Weighted score combining model confidence and nutrition delta.
- `foodbert_score`: Raw model similarity score.
- `nutrition_delta`: Difference in nutrition profile from original.
- `original_nutrition` / `substitute_nutrition`: Nutrition details for comparison.

## Usage

- Call the API with an ingredient and optional restrictions.
- Parse the `ranked_swaps` array to display alternative suggestions to users.
- Use scores and nutrition details to inform user selection.

## Example

```json
{
  "ingredient": "sour cream",
  "rationale": "high fat content",
  "swap_suggestion": {
    "ranked_swaps": [
      {
        "substitute": "greek yogurt",
        "score": 0.92,
        "foodbert_score": 0.95,
        "nutrition_delta": 0.03,
        "original_nutrition": {"calories": 60, "fat": 5, "carbohydrates": 2, "protein": 1},
        "substitute_nutrition": {"calories": 59, "fat": 0.4, "carbohydrates": 3.6, "protein": 10}
      },
      ...
    ]
  }
}
```

## FastAPI Endpoint for UI/API Integration

A FastAPI endpoint is provided in `ingredient_suggestion_api.py` to serve this data for future UI/API use.

### Endpoints

- **GET /suggestions**  
  Returns all swap suggestions.

- **GET /suggestion?ingredient=NAME**  
  Returns swap suggestion for a specific ingredient.

### Example Usage

```bash
uvicorn ingredient_suggestion_api:app --reload
```

- Visit `http://localhost:8000/suggestions` to get all suggestions.
- Visit `http://localhost:8000/suggestion?ingredient=Olive oil` to get suggestions for "Olive oil".

### Integration Notes

- The API serves data directly from `swap_suggestions_official.json`.
- The structure is UI-friendly and ready for REST/GraphQL integration.
- Front-end can easily iterate over `ranked_swaps` and display options, scores, and nutrition.

## References

- [Multi-Ingredient Suggestion PRD](./Multi_Ingredient_Suggestion_PRD.md)
- [Engineering Plan](./Multi_Ingredient_Suggestion_Plan.md)
- [ingredient_suggestion_api.py](../ingredient_suggestion_api.py)
