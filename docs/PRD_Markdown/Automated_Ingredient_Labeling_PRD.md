# Product Requirements Document: Automated Ingredient Labeling for FoodBERT

## 1. Objective

Automate the process of labeling all ingredients in the FoodBERT embedding space with functional categories and dietary tags using Open Food Facts API, to enable fast, accurate, and context-aware ingredient substitution.

---

## 2. Workflow Overview

1. **Export and Normalize FoodBERT Ingredient List**
   - Gather all ingredient names from FoodBERT.
   - Normalize names (lowercase, strip, remove punctuation).

2. **Batch Query Open Food Facts API**
   - For each ingredient, query Open Food Facts for category data.
   - Use product query endpoint (`GET /api/v*/product`) for best coverage.
   - Implement batching:
     - Limit to 100 requests/min for product queries.
     - Limit to 10 requests/min for search queries.
     - Use `time.sleep()` to enforce rate limits.
     - Log failed/missing queries for manual review.

3. **Caching and Retry Logic**
   - Cache results locally after each batch.
   - Retry failed queries up to 2 times, then flag for manual review.

4. **Fill Gaps with LLM or Manual Mapping**
   - For ingredients with missing/ambiguous categories, use ChatGPT/LLM to suggest likely categories.
   - Optionally crowd-source or manually label remaining ingredients.

5. **Multi-Category Tagging**
   - Allow ingredients to have multiple categories (e.g., "zucchini": ["vegetable", "pasta alternative"]).
   - Store all tags in the master ingredient database.

6. **Save Master Ingredient Database**
   - Save enriched ingredient list with categories to a file (e.g., `foodbert_ingredient_categories.json`).
   - Use this file for all future filtering and swap logic.

7. **Periodic Updates**
   - Schedule periodic re-labeling to capture new products or changes in Open Food Facts.

---

## 3. API Rate Limit Handling

- Respect Open Food Facts API limits:
  - 100 req/min for product queries.
  - 10 req/min for search queries.
  - 2 req/min for facet queries.
- No way to bypass limits for public API use.
- For large lists, run script overnight or in multiple sessions.
- For very large projects, consider contacting Open Food Facts for bulk data access.

---

## 4. Metrics for Success

- **Coverage:** >95% of FoodBERT ingredients labeled with at least one functional category.
- **Accuracy:** Manual spot-checking shows >90% correct category assignment.
- **Speed:** Labeling process completes within 24 hours for 10,000 ingredients (with rate limits).
- **Usability:** Master ingredient database enables fast, accurate filtering in substitution workflow.

---

## 5. Implementation Notes

- Use robust normalization and synonym mapping to maximize API match rate.
- Consider multi-threading or async requests (with rate limit enforcement) for efficiency.
- Use LLM fallback for edge cases and ambiguous ingredients.
- Store all results and logs for reproducibility and future updates.

---

## 6. Next Steps

- Implement the labeling script and master database.
- Integrate labeled data into the ingredient substitution workflow.

---

# Progress Marker for Enhanced Ingredient Substitution PRD

**Enhanced_Ingredient_Substitution_PRD.md Progress:**
- All steps up to "Automated Ingredient Labeling" are complete.
- Next step: Integrate labeled ingredient categories into swap candidate filtering and workflow optimization.
