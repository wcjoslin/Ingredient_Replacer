# **Product Requirements Document: Enhanced Ingredient Substitution Engine**

**1. Introduction**

*   **1.1. Problem Statement:** The current ingredient substitution system excels at finding semantically similar ingredients using FoodBERT. However, it does not fully consider the nutritional impact of a substitution or the culinary appropriateness of the swap. This can lead to suggestions that are technically similar but nutritionally unbalanced or nonsensical in a recipe context (e.g., suggesting oil for butter in a frosting recipe).

*   **1.2. Goal:** To evolve the ingredient substitution engine into a holistic system that balances three key pillars: semantic similarity, nutritional equivalence, and culinary context. The system will provide users with smarter, healthier, and more practical ingredient swaps, with a specific focus on modifying recipes for dietary purposes.

*   **1.3. Success Metrics:**
    *   **Relevance Score:** Achieve a 90% or higher relevance score on a curated test set of ingredient swaps, where relevance is defined by a combination of semantic, nutritional, and culinary factors.
    *   **Nutritional Awareness:** For 100% of suggested substitutions, provide a clear summary of the nutritional changes (calories, fat, protein, carbs).
    *   **Culinary Validation:** Successfully filter out at least 95% of known inappropriate swaps from a predefined list of "bad" substitutions based on functional and structural roles.

**2. System Architecture and Data Flow**

The enhanced workflow will be as follows:

1.  **Input:** A recipe, including a list of ingredients, and a potential dietary restriction profile.
2.  **Ingredient Flagging:** Identify which ingredients need to be swapped based on the user's dietary profile or manual selection.
3.  **Candidate Generation (FoodBERT):** For each flagged ingredient, use the existing FoodBERT k-NN model in `ingredient_swap_suggestions.py` to generate a list of the top 5-10 semantically similar substitute candidates.
4.  **Multi-Source Data Enrichment:**
    *   For the original ingredient and all candidates, fetch comprehensive nutritional profiles (calories, protein, fat, carbs) from the USDA API.
    *   Concurrently, gather metadata from Open Food Facts and Suggestic APIs to get ingredient categories or other helpful tags for culinary rule evaluation.
5.  **Nutritional Impact Analysis:**
    *   For each candidate, calculate a `nutrition_delta_score` by comparing its nutritional profile to the original ingredient. This score will quantify the difference in key nutrients.
6.  **Culinary Rule Filtering:**
    *   Apply a rules-based engine to filter out culinarily invalid swaps. This engine will use the enriched metadata and focus on:
        *   **Functional Category Mismatch:** Preventing swaps between categories like `FAT` and `FLOUR`.
        *   **Structural Role Mismatch:** Preventing swaps between `STRUCTURAL` ingredients and `FLAVOR_ENHANCER` ingredients.
7.  **Unified Scoring and Ranking:**
    *   Calculate a final `suggestion_score` for each remaining candidate by combining its `foodbert_similarity_score` and `nutrition_delta_score`.
    *   The formula will be: `final_score = (0.8 * foodbert_score) - (0.2 * nutrition_delta)`.
8.  **Output:** Present the top-ranked substitution to the user in a structured JSON format suitable for a UI layer. The output will include all data necessary to generate a comparative nutrition label.

**3. Feature Requirements**

*   **FR1: Expand USDA Nutritional Data Fetching**
    *   **Description:** The integration with the USDA FoodData Central API must be expanded to retrieve a full nutritional profile, not just carbohydrates.
    *   **Technical Implementation:**
        *   In `usda_api.py`, create a new function `get_food_nutrition_profile(query)` that searches for a food and returns a dictionary containing calories, protein, total fat, and carbohydrates.
        *   Update `integrate_usda_openfoodfacts.py` to use this new function to enrich each ingredient with the full nutritional profile.

*   **FR2: Develop Nutritional Comparison Module**
    *   **Description:** A new module must be created to compare the nutritional profiles of two ingredients and calculate a similarity score.
    *   **Technical Implementation:**
        *   Create a new file: `nutritional_analysis.py`.
        *   Inside, define a function `calculate_nutrition_delta(profile1, profile2)` that takes two nutritional profiles and returns a score.

*   **FR3: Implement a Culinary Rule Engine**
    *   **Description:** An extensible rule engine is needed to prevent obviously incorrect substitutions based on functional and structural roles.
    *   **Technical Implementation:**
        *   Create a new file: `culinary_rules.py`.
        *   Define a function `is_culinarily_valid(original_ingredient, substitute_ingredient, metadata_cache)` that returns `True` or `False`.
        *   The engine will use ingredient metadata to enforce the functional and structural rules.

*   **FR4: Create a Unified Scoring and Ranking System**
    *   **Description:** The final suggestion should be based on a weighted score that combines all factors.
    *   **Technical Implementation:**
        *   In `ingredient_swap_suggestions.py`, modify the logic to calculate the final weighted score.
        *   The culinary check will act as a hard gate: if `is_culinarily_valid` is `False`, the candidate is discarded.

*   **FR5: Refactor the Main Workflow**
    *   **Description:** The main execution script must be updated to orchestrate this new, more complex workflow.
    *   **Technical Implementation:**
        *   Refactor `ingredient_workflow.py` to implement the new data flow. It will call the FoodBERT module, the enrichment module, the nutritional analysis module, and the culinary rules engine in sequence to arrive at the final, ranked suggestions.

---

## **Progress Marker**

**Progress as of 2025-07-15:**
- All steps up to "Automated Ingredient Labeling" are complete.
- Next step: Implement the labeling script and master database as described in `Automated_Ingredient_Labeling_PRD.md`.
- After labeling, integrate labeled ingredient categories into swap candidate filtering and workflow optimization.
