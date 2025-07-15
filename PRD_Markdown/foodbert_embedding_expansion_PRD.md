# FoodBERT Ingredient Embedding Expansion via Suggestic Instructions

## Objective
Increase the number of sentence embeddings for all ingredients in the FoodBERT model with fewer than 40 sentences, using recipe instructions sourced from the Suggestic API (similar to the olive oil workflow).

## Requirements

### Functional
1. **Ingredient Identification**
   - Analyze the current FoodBERT embedding dictionary.
   - Identify all ingredients with fewer than 40 sentence embeddings.

2. **Sentence Expansion Workflow**
   - For each flagged ingredient:
     - Query the Suggestic API for recipes containing the ingredient.
     - Extract up to 40 unique, recipe-relevant instruction sentences mentioning the ingredient.
     - Filter out sentences from ingredient lists or non-instructional content.

3. **Data Integration**
   - Save all expanded sentences for all ingredients in a single file, in the format best suited for updating FoodBERT embeddings.
   - Update the embedding generation workflow to use the expanded sentence set for each ingredient.

4. **Quality Control**
   - Log which ingredients were expanded and how many sentences were added.
   - Optionally, flag ingredients for manual review if fewer than 40 sentences can be found.

5. **Ingredient Prioritization**
   - Treat all flagged ingredients equally; no prioritization will be applied.

### Non-Functional
- The process should be repeatable and scriptable for future expansions.
- API usage should be rate-limited and robust to errors.
- All new/updated data should be versioned and tracked in the repo.

## Deliverables
- A script to identify and expand low-sentence ingredients using Suggestic instructions.
- Updated sentence files for all expanded ingredients.
- Documentation of the workflow and results.
- Optionally, a summary report of before/after sentence counts.

## Out of Scope
- Changing the underlying FoodBERT model architecture.
- Expanding ingredients with >40 sentences.
