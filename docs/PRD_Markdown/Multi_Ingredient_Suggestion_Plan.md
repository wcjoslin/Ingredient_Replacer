# Multi-Ingredient Suggestion Engineering Plan

## Overview
Implement a feature in foodBERT to suggest a ranked list of up to 3 alternative ingredients, with scores and category filtering, allowing users to choose beyond the top suggestion.

## Goals
- Provide users with up to 3 ranked ingredient suggestions.
- Display confidence scores for each suggestion.
- Filter out unreasonable alternatives using category and score thresholds.

## User Stories
- As a user, I want additional ingredient selections if I do not like the first suggestion.
- As a user, I do not want irrelevant options in my recipe.
- As a user, I want to see how close each ranked ingredient is to the original.

## Requirements
- foodBERT must generate a ranked list of up to 3 ingredient suggestions per query.
- Each suggestion must include a confidence score.
- Only suggestions meeting a minimum score and category relevance are shown.
- Do not force 3 suggestions if fewer meet the threshold.

## Acceptance Criteria
- Up to 3 ingredients are returned if they meet scoring and category filters.
- Fewer than 3 are returned if not enough meet the threshold.
- Rankings and scores are visible in the output.

## Engineering Plan
1. **Model Update**: Refactor foodBERT suggestion logic to output a sorted list of top-N (max 3) ingredients per query.
2. **Threshold Logic**: Implement configurable score and category thresholds to filter suggestions.
3. **API/Interface Update**: Update API and UI to display multiple ranked suggestions with scores.
4. **Documentation**: Document new API endpoints, data structures, and usage examples.
5. **Testing**:
    - Write unit tests for ranking, filtering, and threshold logic.
    - Write integration tests for end-to-end suggestion workflow.
    - Achieve at least 80% test coverage for new modules.
    - Include edge cases (e.g., fewer than 3 valid suggestions, all suggestions below threshold).
6. **Version Control**: Use Git for all changes, with clear commit messages and PRs.
7. **Code Standards**: Follow project coding conventions and naming standards.

## Test Plan
- **Unit Tests**: Validate ranking, filtering, and threshold logic.
- **Integration Tests**: Ensure correct output from API/UI for various input scenarios.
- **Edge Cases**: Test with 0, 1, 2, and 3 valid suggestions; test with all suggestions below threshold.
- **Negative Tests**: Ensure no extraneous or irrelevant suggestions are returned.

## References
- [Multi-Ingredient Suggestion PRD](./Multi_Ingredient_Suggestion_PRD.md)
- [Notion Task](https://www.notion.so/Multi-Ingredient-Suggestion-238595a1a57880b4a559c23dedbe6987)
- COPILOT_INSTRUCTIONS.md
