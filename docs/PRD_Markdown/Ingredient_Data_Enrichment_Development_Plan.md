# Diet Rules & Ingredient Highlight - Development Plan (Expanded from MCP)

## Objective

Enhance the frontend app to:
- Surface the active dietary rules and restrictions for each selected diet (fetched from backend).
- Visually highlight which ingredients will be replaced, and why.
- Provide full context for users about nutrition, categories, and the logic behind swaps.

---

## Requirements (from MCP)

### 1. Diet Rule Summaries
- On diet selection, show a summary of each selected diet:
  - **Description**: What the diet is and its goal.
  - **Explicit category restrictions** (e.g., "No dairy", "No meats").
  - **Explicit macronutrient restrictions** (e.g., "Max 10g carbs per ingredient").

### 2. Ingredient Feedback & Highlighting
- For each ingredient:
  - Show nutrition facts and categories as bullet points below the ingredient.
  - If the ingredient will be swapped:
    - Highlight the ingredient in a different color.
    - Highlight the specific nutrition or category info that is causing the swap in a different color.
    - Show a tooltip or inline note explaining what is non-compliant (e.g., "Exceeds carb limit", "Category: Meats excluded").
    - Show a description of the dietary change being made (e.g., "Lowering total carbs") above the swap suggestion list.
    - **If an ingredient is flagged for multiple reasons, show all relevant highlights/rationales.**

### 3. Visual Cues & Explanations
- Visual cues (color, icon, etc.) for:
  - Ingredients being swapped.
  - The specific reason for the swap (nutrition or category).
- Legend for highlight system.
- No click/drilldown required, but tooltips for rationale.
- **If rules are long, truncate with tooltip for full text.**

### 4. Dietary Change Summary
- **Show a summary of all dietary changes at the top of the page.**

---

## User Stories

- As a user, I want to see what nutrition information is causing my ingredient to be swapped out.
- As a user, I want to know what dietary category restriction is causing my ingredient to be swapped out.
- As a user, I want to see the nutritional and categorical breakdown of my ingredients so I can have full context into what is changing.
- As a user, I want a visual cue of what ingredients are being swapped out so I know what to look for in the new recipe.
- As a user, I want a visual cue of what part of the ingredient is causing the swap so I can follow the logic of the change.
- As a user, I want a description of the change that needs to be made to the recipe ingredients so I know what goal is being achieved.

---

## Acceptance Criteria

- Nutrition facts and categories of each ingredient are shown as bullet points below each ingredient.
- Ingredients to be swapped are highlighted in a different color.
- Nutrition or category info causing a swap is highlighted in a different color from the rest.
- Description of the dietary change being made is given above the swapped ingredient suggestion list.
- **A summary of all dietary changes is shown at the top of the page.**
- **If an ingredient is flagged for multiple reasons, all relevant highlights/rationales are shown.**
- **If rules are long, they are truncated with tooltip for full text.**

---

## Implementation Steps

### Backend
- [ ] Add endpoint to return diet summaries, category restrictions, and macronutrient rules for each diet.
- [ ] Ensure swap/enrichment API returns:
  - For each ingredient: nutrition, categories, swap rationale (nutrition/category), and description of dietary change.

### Frontend
- [ ] On diet selection, fetch and display:
  - Diet summary, category restrictions, macronutrient restrictions.
  - **Summary of all dietary changes at the top of the page.**
- [ ] For each ingredient:
  - Show nutrition and categories as bullet points.
  - If flagged for swap:
    - Highlight ingredient.
    - Highlight specific bullet(s) causing swap.
    - Tooltip or inline note for rationale.
    - **Show all relevant highlights/rationales if flagged for multiple reasons.**
- [ ] Show description of dietary change above swap suggestions.
- [ ] Add legend for highlight system.
- [ ] **Truncate long rules with tooltip for full text.**

### Testing
- [ ] Manual test: Select diets, verify summaries, highlights, tooltips, and descriptions.
- [ ] Test with multiple diets and edge cases (e.g., ingredient flagged for multiple reasons, long rules).

---

## Suggestions / Questions

- Consider accessibility for colorblind users (use icons or patterns in addition to color).

---

**Let me know if you want to adjust any requirements or need help with backend or frontend implementation details!**
