# Ingredient Data Enrichment – Step-by-Step Implementation Checklist

## Branching & Setup
- [ ] Create a new feature branch from `main` (e.g., `feature/ingredient-data-enrichment`).

## Data Enrichment Logic
- [ ] Identify or create the enrichment module/function.
- [ ] Load `data enrichment/enriched_ingredient_data_nutritionix.json` for nutritional data.
- [ ] Load `foodbert_ingredient_categories_merged.json` for categorical/dietary data.
- [ ] Load `dietary_restriction_presets.json` for dietary restriction rules.
- [ ] For each ingredient in the uploaded recipe:
    - [ ] Normalize/clean ingredient names for lookup.
    - [ ] Look up nutrition facts (calories, protein, carbs, fat) from Nutritionix file.
    - [ ] Look up all dietary category flags from foodBERT categories file.
    - [ ] Apply dietary restriction flagging logic using presets/rules.
    - [ ] Aggregate nutrition and category results.
    - [ ] If ingredient is missing from reference files, add note:  
          "Nutritional Information for <Ingredient> is incomplete at this time, unable to find dietary information at this time".
    - [ ] Format output: nutrition facts first, then all category flags.

## API/Backend Integration
- [ ] Ensure enrichment is triggered synchronously during recipe upload.
- [ ] Format and return a bullet-point list per ingredient with dietary info.

## Error Handling
- [ ] Gracefully handle missing/partial data from any/all sources.
- [ ] Ensure partial results are returned if only some data is available.

## Testing
- [ ] Unit tests for enrichment logic (mocking file reads, not APIs).
- [ ] Integration tests for recipe upload and enrichment.
- [ ] Manual test: Upload recipes with common, rare, and unknown ingredients.

## Documentation
- [ ] Update README with enrichment workflow and output example.
- [ ] Update API documentation to specify new/updated endpoints and response format.

## Pull Request
- [ ] Push feature branch and open a PR to `main`.
- [ ] Ensure all tests pass and request review.
- [ ] Merge only after review and successful checks.

---

Check off each item as you complete it to track progress!
