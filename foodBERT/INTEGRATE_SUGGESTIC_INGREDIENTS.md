# Integrating Suggestic Ingredients with foodBERT

## Overview

This guide explains how to use the normalized ingredient list from Suggestic (foodbert_ready_ingredients.json) to extend the embedding space of foodBERT.

## Steps

1. **Copy the Ingredient List**
   - Ensure `foodbert_ready_ingredients.json` is available in the foodBERT directory or a known path.

2. **Prepare for Embedding Generation**
   - Use or adapt the script `foodbert_embeddings/helpers/generate_ingredient_embeddings.py` to load the new ingredient list.
   - Example: Modify the script to read from `foodbert_ready_ingredients.json` and generate embeddings for each ingredient.

3. **Generate Embeddings**
   - Run the embedding generation script with the new ingredient list.
   - Example (pseudo-code):
     ```python
     import json
     from foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_embeddings

     with open("foodbert_ready_ingredients.json", "r", encoding="utf-8") as f:
         ingredients = json.load(f)

     embeddings = generate_embeddings(ingredients)
     # Save or use embeddings as needed
     ```

4. **Validate Integration**
   - Confirm that embeddings are generated for all new ingredients.
   - Optionally, run test cases or similarity checks to validate embedding quality.

## Notes

- You may need to adapt foodBERT scripts to accept a custom ingredient list.
- Refer to `foodbert_embeddings/README.md` for more details on embedding generation.
