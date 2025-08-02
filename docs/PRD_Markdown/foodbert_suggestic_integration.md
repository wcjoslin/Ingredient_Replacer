# Suggestic–foodBERT Ingredient Substitution Integration Plan

## Objective

Create a reusable function to:
- Query a recipe from the Suggestic API by ID.
- Extract the list of ingredients.
- Use foodBERT to suggest a substitute for a given ingredient (starting with the first ingredient).
- Output the substitution result as a JSON file.
- Log errors for ingredients not present in the embedding vocabulary, with enough information for future embedding addition.

---

## Step-by-Step Implementation Plan

### 1. Query Recipe from Suggestic

- Use the `query_suggestic` function to send a GraphQL query for a recipe by its ID.
- Parse the API response to extract the list of ingredients.

### 2. Extract Ingredient(s)

- Select the first ingredient from the recipe’s ingredient list.
- (Future-proof: allow for other ingredient swaps by parameterizing the function.)

### 3. Generate Embedding for Ingredient

- Use foodBERT’s embedding utilities to generate or retrieve the embedding for the selected ingredient.
- If the ingredient is not found in the embedding vocabulary:
  - Log an error with the ingredient name and recipe context.
  - Skip substitution for this ingredient.

### 4. Find Substitute Using foodBERT

- Initialize the ApproxKNNClassifier with all available ingredient embeddings.
- Use the classifier to find the nearest neighbor (substitute) for the ingredient.
- Retrieve the substitute name and the model’s confidence/score (distance or similarity).

### 5. Output Results

- Write the following to a JSON file:
  - Original ingredient
  - Suggested substitute
  - Model confidence/score
  - Recipe ID and name for context

### 6. Error Logging

- For any ingredient not found in the embedding space, log:
  - Ingredient name
  - Recipe ID and name
  - Full ingredient list (for context)
- Save error logs to a separate file for future embedding updates.

---

## Notes

- The function should be reusable for any ingredient in any recipe.
- Output format should be consistent and machine-readable (JSON).
- Error logs should be clear and actionable for future embedding expansion.

---

## Next Steps

- Implement the integration function as described.
- Ensure all dependencies (Suggestic API, foodBERT, classifier) are properly initialized.
- Test with the provided recipe example and validate output.
