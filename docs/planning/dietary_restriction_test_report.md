# Product Requirements Document (PRD): Ingredient Replacer Dietary Restriction Test

## Objective
Test the ingredient swap functionality for common dietary restrictions using popular recipes from the Suggestic platform, and document missing ingredient coverage for future embedding improvements.

---

## Step-by-Step Plan

### 1. Query Popular Recipes
- Use Suggestic API to fetch a list of popular recipes (name, id).
- **Output:** `popular_recipes.json` containing recipe names and IDs.

### 2. Dietary Restriction Tests
For each user story (pre-diabetic, vegan, kosher):
- Select a suitable recipe.
- Identify ingredients that violate the restriction.
- Swap only the necessary ingredients using FoodBERT, minimizing changes.
- If an ingredient is missing from the embedding vocabulary:
  - Attempt to find a synonym.
  - If no synonym, log the missing ingredient and its cooking instructions.
- **Outputs:**
  - `diet_test_results.json` containing:
    - Recipe ID, name, original ingredients, swapped ingredients, restriction type, and swap rationale.
  - `missing_ingredients.json` containing:
    - Missing ingredient name, recipe ID, recipe name, and relevant cooking instructions.

### 3. Documentation
- Summarize the process and results in a markdown file.
- **Output:** `dietary_restriction_test_report.md` with:
  - Overview of methodology.
  - Summary of swaps performed.
  - List of missing ingredients and next steps for embedding updates.

---

## Outputs to be created
- `popular_recipes.json`
- `diet_test_results.json`
- `missing_ingredients.json`
- `dietary_restriction_test_report.md`
