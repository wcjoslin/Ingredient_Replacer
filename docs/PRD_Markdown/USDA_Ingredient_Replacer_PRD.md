# Product Requirements Document (PRD): USDA-Enhanced Ingredient Replacer Workflow

## Objective
Enable users to query recipes, apply multiple dietary restrictions, and use the USDA FoodData Central API to inform ingredient swaps with nutrition-aware logic, integrating with FoodBERT for optimal substitutions.

---

## Workflow Steps

### 1. Recipe Query
- User queries for a recipe (via Suggestic or other source).
- System retrieves recipe details, including ingredients, instructions, and nutrition summary.

### 2. Dietary Restriction Input
- User specifies one or more dietary restrictions (e.g., low-carb, vegan, kosher, low-sodium, allergies).
- Restrictions can include macronutrients, micronutrients, minerals, and other health or religious requirements.

### 3. Ingredient Nutrition & Metadata Lookup
- For each ingredient in the recipe, query the USDA FoodData Central API for detailed nutrition data.
- Query the Open Food Facts API for dietary metadata (vegan, vegetarian, kosher, halal, allergen info, etc.).
- Extract relevant nutrient values (carbs, protein, fat, sugar, sodium, vitamins, minerals, etc.) and metadata tags.
- Store ingredient nutrition and metadata in a structured format (JSON).
- Implement parallelization of API calls to reduce latency.
- Add caching and batching of ingredient queries for efficiency.
- Respect API rate limits and implement request throttling.

### 4. Restriction Analysis & Swap Logic
- Analyze each ingredient against all user-specified restrictions using nutrition and metadata.
- Identify ingredients that violate restrictions.
- Use FoodBERT to suggest substitutes, prioritizing options that best fit the nutrition and restriction criteria.
- Automatically select the best swap based on USDA nutrition data, Open Food Facts metadata, and FoodBERT similarity.

### 5. Recipe Update & Output
- Update the recipe with swapped ingredients.
- Output updated recipe, ingredient list, nutrition summary, and rationale for each swap.
- Use JSON format for data exchange between steps and APIs.

### 6. Future Steps (TODO)
- Add user-facing review and approval step for suggested swaps.
- Implement caching for USDA API results.
- Support batch queries and more advanced restriction logic.

---

## Outputs
- Updated recipe with ingredient swaps and nutrition summary (JSON).
- Per-ingredient nutrition data (JSON).
- Swap rationale and restriction compliance report (JSON/Markdown).
- Logs and error reports as needed.

---

## Notes
- Workflow supports multiple simultaneous dietary restrictions.
- USDA API is used for all nutrition-related restrictions.
- Data formats are chosen for compatibility and ease of integration (JSON recommended).
- User review step is deferred to future development.
