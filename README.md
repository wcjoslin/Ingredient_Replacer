# Ingredient Replacer App

## Features

- Upload a recipe URL and extract ingredients
- Highlight ingredients flagged for dietary restrictions
- Suggest ingredient swaps for selected diets
- Display diet summaries and ingredient nutrition
- **NEW:** Generate and display FDA-style nutrition label for uploaded recipes

## Nutrition Label Feature

- Backend API: `/nutrition-label` (see `nutrition_label_api.py`)
  - Accepts: JSON with `ingredients` (list) and `servings` (int)
  - Returns: base64-encoded PNG image and nutrition summary
- Frontend: Displays nutrition label image above ingredient list after recipe upload

## How to Use

1. Start the backend API:
   ```
   python nutrition_label_api.py
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
   - Suggest swaps
   - Show diet summaries
   - **Show a nutrition label image above the ingredient list**

## Testing

- Run backend tests:
  ```
  pytest tests/test_nutrition_label_api.py
  ```
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

## Requirements

- Python 3.10+ (for backend)
- Node.js 18+ (for frontend)
- Flask, flask-cors, Pillow, pytest
