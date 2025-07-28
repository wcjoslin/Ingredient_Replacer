# Ingredient Replacer – Recipe Upload Feature

## Overview

This project allows users to upload recipes and receive ingredient suggestions or replacements based on dietary preferences and other criteria.

---

## Setup Instructions

### Backend (FastAPI)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the API server:**
   ```bash
   uvicorn ingredient_suggestion_api:app --reload
   ```
3. **Ensure required model/data files are present:**
   - `foodBERT/foodbert_embeddings/data/food_embeddings_dict_foodbert_combined.pkl` (not tracked by git, must be present locally)

### Frontend (Next.js/React)

1. **Navigate to the frontend directory:**
   ```bash
   cd app-landing-page
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm run dev
   ```
4. **Access the app:**
   - Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Recipe Upload Workflow

1. User uploads a recipe file via the frontend.
2. Frontend sends the file to the backend API.
3. Backend processes the recipe and returns ingredient suggestions.
4. Frontend displays the results to the user.

---

## API Documentation

See [API_DOCS.md](API_DOCS.md) for full details.

**Main Endpoint:**

### POST `/suggestions`
- **Request:** JSON body with `ingredients` (array of strings) and optional `diets` (array of strings).
- **Response:** JSON with swap suggestions for each ingredient.

---

## Environment Variables

- `.env` file should contain any secrets, API keys, or configuration values.
- Example:
  ```
  API_URL=http://localhost:8000
  ```

---

## Testing

### Backend

- Run backend tests:
  ```bash
  pytest tests/test_recipe_upload_api.py
  ```

### Frontend

- Run frontend tests:
  ```bash
  cd app-landing-page
  npm test
  ```

---

## Contributing

- Ensure `.gitignore` excludes large data/model files, node_modules, and cache files.
- Do not commit `node_modules` or `.pyc` files.
- Document new features and API changes.

---

## Unfinished Steps (for future tasks)

- Add real frontend and backend tests for all major features.
- Expand API documentation as new endpoints are added.
- Set up CI/CD for automated testing and deployment.

---

## License

MIT
