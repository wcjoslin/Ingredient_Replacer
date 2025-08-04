# Ingredient Extraction Service Enhancement Plan

---

## Overview

Upgrade the ingredient parsing workflow to robustly extract core ingredient names from recipe uploads using a hybrid rule-based and spaCy NLP approach. This will improve accuracy for enrichment and downstream tasks by removing quantities, units, and preparation instructions.

---

## Goals

- Accurately extract ingredient names from varied recipe phrasing.
- Remove extraneous words (quantities, units, preparation instructions).
- Integrate spaCy NLP for noun phrase extraction.
- Maintain compatibility with foodBERT vocabulary and enrichment pipeline.

---

## Motivation

Current normalization leaves in extra words (e.g., "cucumber cut into pieces"), causing noisy enrichment and poor matching. Many recipes use inconsistent phrasing, so a more sophisticated extraction is needed.

---

## Requirements

- Strip quantities and units using regex.
- Remove preparation instructions and adjectives.
- Use spaCy to extract the main noun/noun phrase.
- Validate against foodBERT vocabulary.
- Update tests to cover new edge cases.

---

## User Stories

- As a user, I want ingredient names to be clean and accurate for nutrition and swap suggestions.
- As a developer, I want the extraction logic to handle diverse recipe formats.
- As a data scientist, I want reliable ingredient mapping for enrichment.

---

## Acceptance Criteria

- "cucumber cut into pieces" → "cucumber"
- "¼ teaspoon black pepper" → "black pepper"
- "2 cups shredded cheddar cheese" → "cheddar cheese"
- All test cases pass with correct normalization.
- No extraneous words remain in extracted ingredient names.

---

## Engineering Plan

1. **Preprocessing (Rule-Based)**
   - Expand regex in `normalize_ingredient_string` to strip quantities, units, and common preparation phrases.
   - Maintain a list of units and prep terms for removal.

2. **spaCy NLP Extraction**
   - Add a new function (e.g., `extract_core_ingredient_spacy`) to run spaCy on cleaned strings.
   - Extract the main noun/noun phrase, filtering out adjectives, verbs, and prep instructions.

3. **Integration**
   - Refactor `map_ingredients_to_foodbert` to use the new hybrid extraction before fuzzy matching.
   - Ensure compatibility with foodBERT vocabulary.

4. **Testing**
   - Update `tests/test_ingredient_workflow.py` with new cases and edge scenarios.
   - Achieve high coverage for normalization and extraction logic.

5. **Documentation**
   - Update developer notes and README to describe new workflow.

6. **Dependencies**
   - Ensure spaCy is listed in `requirements.txt` and properly configured.

---

## Impact

- Improved ingredient enrichment and nutrition analysis.
- Cleaner ingredient data for swaps and dietary restriction logic.
- Reduced manual post-processing.

---

## Risks

- spaCy may misclassify rare ingredient phrases; fallback to rule-based logic as needed.
- Regex changes may affect legacy parsing; test thoroughly.

---

## Files to Change

- `src/ingredient_workflow.py` (main logic)
- `tests/test_ingredient_workflow.py` (unit tests)
- `requirements.txt` (dependency check)
- Documentation files (README.md, developer notes as needed)

---

## References

- COPILOT_INSTRUCTIONS.md (template)
- foodBERT vocabulary
- spaCy documentation

---
