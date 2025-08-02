# foodBERT Ingredient Prefiltering PRD

## Overview
The foodBERT model currently compares user-submitted recipe ingredients against a library of ~450 ingredients. Filtering based on categorical mismatches is possible, but the process still incurs significant runtime. Since all ingredients are categorized before being processed, we can pre-filter nonsensical replacements (e.g., Spices for Meats) before passing the list to foodBERT, improving efficiency.

## Goals
- Pre-filter the list of candidate ingredients for foodBERT based on ingredient categories.
- Reduce model runtime and improve user experience by minimizing unnecessary comparisons.

## User Stories
- As a shopper, I want ingredient replacements quickly so I can continue my grocery shopping without delay.
- As the app owner, I want to minimize computational workload while maintaining high-quality replacement suggestions.

## Requirements
- Implement a pre-filtering mechanism that excludes ingredients from categories that do not match the target ingredient's category.
- Ensure that only sensible replacement candidates are passed to foodBERT for assessment.
- Maintain compatibility with existing ingredient categorization logic.

## Acceptance Criteria
- The pre-filtering logic excludes nonsensical replacements (e.g., Spices for Meats) before foodBERT assessment.
- Model runtime for ingredient replacement suggestions is measurably reduced.
- Replacement suggestions remain relevant and high quality.
- Unit and integration tests cover at least 80% of the new filtering logic, including edge cases.

## Engineering Plan
- Analyze current ingredient categorization and replacement workflow.
- Design and implement a filtering function/module to exclude mismatched categories.
- Integrate the filtering step into the foodBERT ingredient assessment pipeline.
- Refactor and document code as needed to maintain clarity and compatibility.
- Write unit and integration tests for the filtering logic.

## Test Plan
- Develop unit tests for the filtering function, including edge cases (e.g., ambiguous categories, missing category data).
- Create integration tests to verify correct operation within the foodBERT pipeline.
- Measure and report runtime improvements before and after pre-filtering.
- Validate that replacement suggestions remain relevant and sensible after filtering.
