# Diet Rules & Ingredient Highlight - Implementation Checklist

This checklist breaks down the development plan into actionable backend and frontend tasks, with testing and polish steps.

---

## Backend

- [ ] Add endpoint to return diet summaries, category restrictions, and macronutrient rules for each diet.
    - [ ] Include: diet description, category restrictions, macronutrient restrictions.
    - [ ] Support truncation/tooltip for long rules.
- [ ] Update swap/enrichment API to return for each ingredient:
    - [ ] Nutrition facts and categories.
    - [ ] Swap rationale(s): all reasons (nutrition/category) for being flagged.
    - [ ] Description of dietary change for each flagged ingredient.
    - [ ] Support multiple rationales per ingredient.

---

## Frontend

- [ ] On diet selection:
    - [ ] Fetch and display diet summary, category restrictions, macronutrient restrictions.
    - [ ] Show summary of all dietary changes at the top of the page.
    - [ ] Truncate long rules with tooltip for full text.
- [ ] Ingredient list:
    - [ ] Show nutrition facts and categories as bullet points below each ingredient.
    - [ ] If ingredient is flagged for swap:
        - [ ] Highlight ingredient in a different color.
        - [ ] Highlight specific bullet(s) (nutrition/category) causing swap in a different color.
        - [ ] Show all relevant highlights/rationales if flagged for multiple reasons.
        - [ ] Tooltip or inline note for rationale(s).
- [ ] Above swap suggestions:
    - [ ] Show description of dietary change being made.
- [ ] Add legend for highlight system (color/icon meanings).
- [ ] Ensure accessibility (icons/patterns for colorblind users).

---

## Testing

- [ ] Manual test: Select diets, verify summaries, highlights, tooltips, and descriptions.
- [ ] Test with:
    - [ ] Multiple diets selected.
    - [ ] Ingredients flagged for multiple reasons.
    - [ ] Long rules (truncation/tooltip).
    - [ ] Accessibility (colorblind, screen reader).
- [ ] Confirm acceptance criteria from plan are met.

---

## Polish & Review

- [ ] Review UI for clarity and usability.
- [ ] Review API responses for completeness and consistency.
- [ ] Update documentation (README, API_DOCS) as needed.

---

**Check off each item as you complete it. Let me know if you want to expand any step into sub-tasks or need code scaffolding for any part!**
