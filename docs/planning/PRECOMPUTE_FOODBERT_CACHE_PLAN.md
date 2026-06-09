# COPILOT INSTRUCTIONS – Precompute foodBERT Results & Cache Integration

---

## Objective

Transition the app to use precomputed foodBERT swap suggestions for all ingredients in `foodBERT/foodbert/data/used_ingredients.json`, eliminating live model inference during recipe upload. Maintain existing app behavior and API structure.

---

## Step-by-Step Plan

### 1. Precompute foodBERT Results

- **Script Creation:**  
  - Create a new script: `foodBERT/foodbert_embeddings/precompute_foodbert_swaps.py`
  - This script will:
    - Load all ingredients from `foodBERT/foodbert/data/used_ingredients.json`
    - For each ingredient, run the foodBERT swap suggestion logic (reference: `foodBERT/foodbert_embeddings/generate_substitutes.py`)
    - Save results in a cache file: `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`

- **References:**  
  - `foodBERT/foodbert_embeddings/generate_substitutes.py` (core swap logic)
  - `foodBERT/foodbert/data/used_ingredients.json` (ingredient list)

### 2. Integrate Cache into API Workflow

- **Modify API Layer:**  
  - Update backend API code responsible for swap suggestions:
    - Likely files:  
      - `src/ingredient_swap_suggestions.py` (swap logic)
      - `src/ingredient_suggestion_api.py` (API endpoint)
    - On API startup, load `foodBERT/foodbert_embeddings/foodbert_swap_cache.json` into memory (e.g., Python dict).
    - When a swap suggestion is requested, check cache first:
      - If ingredient is in cache, return cached result.
      - If not, return a default response or error (no live inference).

- **References:**  
  - `src/ingredient_swap_suggestions.py` (main swap logic)
  - `src/ingredient_suggestion_api.py` (API endpoint)
  - `API_DOCS.md` (API contract)

### 3. Maintain Existing Behavior

- **API Contract:**  
  - Ensure API responses match current structure (see `API_DOCS.md`).
  - If an ingredient is not in cache, return a clear message (e.g., "No swap suggestion available for this ingredient").

- **Testing:**  
  - Update or add tests in `tests/test_ingredient_data_enrichment.py` and `tests/test_recipe_upload_api.py` to verify cache-based swap suggestions.

### 4. Documentation

- **Update README:**  
  - Document the new caching workflow in `README.md` and `API_DOCS.md`.
  - Add instructions for running the precompute script and updating the cache.

- **Reference Files:**  
  - `README.md`
  - `API_DOCS.md`
  - `COPILOT_INSTRUCTIONS.md` (this plan)

---

## File Summary

- **New:**  
  - `foodBERT/foodbert_embeddings/precompute_foodbert_swaps.py`  
  - `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`

- **Modified:**  
  - `src/ingredient_swap_suggestions.py`
  - `src/ingredient_suggestion_api.py`
  - `README.md`
  - `API_DOCS.md`
  - `tests/test_ingredient_data_enrichment.py`
  - `tests/test_recipe_upload_api.py`

- **Referenced:**  
  - `foodBERT/foodbert_embeddings/generate_substitutes.py`
  - `foodBERT/foodbert/data/used_ingredients.json`
  - `COPILOT_INSTRUCTIONS.md`

---

## Notes

- No live foodBERT inference will occur during API requests.
- For new ingredients, update the cache by rerunning the precompute script.
- App behavior and API responses should remain unchanged except for improved speed and reliability.

---

## Next Steps

1. Implement the precompute script.
2. Integrate cache loading and lookup in API workflow.
3. Update documentation and tests.
4. Validate end-to-end behavior.
