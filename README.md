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

## API Endpoints

### `POST /upload-recipe`
- **Description:** Upload a recipe file and receive ingredient suggestions.
- **Request:** Multipart/form-data with recipe file.
- **Response:** JSON with suggested ingredients and replacements.

### `GET /ingredient-suggestions`
- **Description:** Get ingredient suggestions for a given recipe.
- **Request:** Query parameters or JSON body.
- **Response:** JSON with suggestions.

---

## Environment Variables

- `.env` file should contain any secrets, API keys, or configuration values.
- Example:
  ```
  API_URL=http://localhost:8000
  ```

---

## Testing

### Manual Testing

- Upload valid and invalid recipe files.
- Test with different dietary restrictions.
- Check error handling and UI feedback.

### Automated Testing

- Backend: Use `pytest` for API endpoint tests.
- Frontend: Use `Jest` and `React Testing Library` for component and integration tests.

---

## Contributing

- Ensure `.gitignore` excludes large data/model files, node_modules, and cache files.
- Do not commit `node_modules` or `.pyc` files.
- Document new features and API changes.

---

## Unfinished Steps (for future tasks)

- Remove any committed `node_modules` folders from git history.
- Clean up large data/model files from git history if needed.
- Add automated unit and integration tests for backend and frontend.
- Add OpenAPI/Swagger documentation for backend API.
- Push all staged changes to GitHub.

---

## License

MIT
