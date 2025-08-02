# Multi-Ingredient Suggestion PRD

## Context
The foodBERT model currently assesses ingredients from its library and returns its highest scored suggestion. While this is good for a speedy implementation, it may leave users wanting if they do not like the suggestion. The goal is to increase the number of ingredients the model suggests, allowing users to select alternatives beyond the top choice.

## Goals
- Create a ranked list of up to 3 ingredients from the model’s suggestions to give users additional choices.
- Provide users with additional choices in case they do not like the initial selection.
- Display ranks and scores for each ingredient to show confidence in selection.
- Implement a lower threshold for ingredient selections in case a 2nd or 3rd option is not reasonable.

## User Stories
- As a user, I want additional ingredient selections in case I do not like the first suggestion.
- As a user, I do not want extraneous options if they would not make sense in my recipe.
- As a user, I want to know how close each ranked ingredient is, to decide if my recipe would be better suited with the first suggestion or others in the list.

## Acceptance Criteria
- Return up to 3 ingredients if they all achieve the scoring threshold and category filtering.
- Do not force 3 ingredients to be returned if fewer than 3 meet the threshold.
- Ranking is visible as part of the output.
