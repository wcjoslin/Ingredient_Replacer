# Recipe Nutrition Label Development Plan

## 1. Task Summary
Generate a nutrition label image for uploaded recipes, summing nutrition facts from all ingredients and providing drill-down per ingredient. Use internal nutrition data only.

## 2. Requirements
- Nutrition label generated as an image (not HTML).
- Nutrition facts summed for the whole recipe.
- Drill-down option for each ingredient's nutrition.
- Nutrition fields: calories, protein, fat, carbs, micronutrients (if available).
- Per-recipe nutrition; compare ingredient servings if possible.
- Use `data enrichment/enriched_ingredient_data_nutritionix.json` as the data source.
- No external API calls.
- Acceptance: correct summing, correct label format, drill-down per ingredient.

## 3. Implementation Steps
1. Create a feature branch (e.g., `feature/recipe-nutrition-label`).
2. Parse uploaded recipe and extract ingredient list and servings.
3. For each ingredient, retrieve nutrition data from `enriched_ingredient_data_nutritionix.json`.
4. Sum nutrition facts for the whole recipe, adjusting for servings.
5. Research and select a library for generating nutrition label images (e.g., Python Pillow, Node Canvas, or React SVG).
6. Implement logic to generate a nutrition label image in the standard format.
7. Add drill-down functionality to show ingredient-level nutrition breakdown.
8. Integrate image generation into the recipe upload workflow.
9. Save or display the generated image as required.

## 4. Testing
- Unit tests for nutrition summing logic.
- Integration tests for image generation.
- Manual testing with sample recipes and ingredient data.

## 5. Documentation
- Update README with usage instructions for nutrition label feature.
- Document any new scripts, modules, or endpoints.

## 6. Pull Request
- All changes made in a feature branch.
- Open PR to `main` after testing and documentation.
- Ensure review and successful checks before merging.
