# Ingredient Replacer App

## Features

- Upload a recipe URL and extract ingredients
- Highlight ingredients flagged for dietary restrictions
- Suggest ingredient swaps for selected diets
- Display diet summaries and ingredient nutrition
- **NEW:** Generate and display FDA-style nutrition label for uploaded recipes
- **NEW:** Ingredient swap suggestions now use a precomputed foodBERT cache for fast, reliable results

## Nutrition Label Feature

- Backend API: `/nutrition-label` (see `src/nutrition_label_api.py`)
  - Accepts: JSON with `ingredients` (list) and `servings` (int)
  - Returns: base64-encoded PNG image and nutrition summary
- Frontend: Displays nutrition label image above ingredient list after recipe upload

## Ingredient Swap Suggestions (foodBERT-powered)

- Backend API: `/suggestions` (see `src/ingredient_suggestion_api.py`)
  - Accepts: JSON with `ingredients` (list) and optional `diets` (list)
  - Returns: swap suggestions for flagged ingredients, using precomputed cache
- **Performance:** Swap suggestions are now instant, using `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`
- **Cache Regeneration:** To update swap suggestions for new ingredients, run `foodBERT/foodbert_embeddings/precompute_foodbert_swaps.py` to regenerate the cache.

## How to Use

1. Start the backend API:
   ```
   uvicorn src.ingredient_suggestion_api:app --reload
   ```
   (Requires `fastapi`, `uvicorn`, and other dependencies)

   For nutrition label API:
   ```
   python src/nutrition_label_api.py
   ```
   (Requires `flask` and `flask-cors`)

2. Start the frontend app:
   ```
   npm run dev
   ```
   (or `yarn dev`)

3. Paste a recipe URL and submit. The app will:
   - Extract ingredients
   - Highlight flagged items
   - Suggest swaps (using foodBERT cache)
   - Show diet summaries
   - **Show a nutrition label image above the ingredient list**

## Testing

- Run backend tests:
  ```
  pytest tests/
  ```
  (or run individual test files, e.g. `pytest tests/test_nutrition_label_api.py`)
- Run frontend tests:
  ```
  npm test
  ```

## API Reference

### POST `/nutrition-label`
Request:
```json
{
  "ingredients": ["egg", "milk"],
  "servings": 2
}
```
Response:
```json
{
  "nutrition_label_image": "<base64 PNG>",
  "nutrition_summary": { ... }
}
```

### POST `/suggestions`
Request:
```json
{
  "ingredients": ["egg", "milk"],
  "diets": ["keto", "vegan"]
}
```
Response:
```json
{
  "suggestions": [
    {
      "original": "egg",
      "categories": [...],
      "display_categories": [...],
      "dietary_flags": [...],
      "swap_suggestion": {
        "ranked_swaps": [
          {"substitute": "tofu", "score": 0.92, ...}
        ]
      }
    }
  ]
}
```

## Requirements

- Python 3.10+ (for backend)
- Node.js 18+ (for frontend)
- Flask, flask-cors, FastAPI, uvicorn, Pillow, pytest

## Updating the foodBERT Swap Cache

- If you add new ingredients or want to refresh swap suggestions:
  1. Run: `python foodBERT/foodbert_embeddings/precompute_foodbert_swaps.py`
  2. This will regenerate `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`
  3. Restart the backend API to load the new cache
