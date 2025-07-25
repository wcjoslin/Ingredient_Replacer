# ingredient_suggestion_api.py
# Simple FastAPI endpoint to serve multi-ingredient suggestions for future UI integration

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import json

app = FastAPI(title="Multi-Ingredient Suggestion API")

# Load swap suggestions at startup
with open("swap_suggestions_official.json", "r", encoding="utf-8") as f:
    SUGGESTIONS = json.load(f)

@app.get("/suggestions")
def get_all_suggestions():
    """
    Return all ingredient swap suggestions.
    """
    return JSONResponse(content=SUGGESTIONS)

@app.get("/suggestion")
def get_suggestion(ingredient: str = Query(..., description="Ingredient name to query")):
    """
    Return swap suggestion for a specific ingredient.
    """
    ingredient_lower = ingredient.lower().strip()
    for entry in SUGGESTIONS:
        if entry["ingredient"].lower().strip() == ingredient_lower:
            return JSONResponse(content=entry)
    return JSONResponse(content={"error": f"No swap suggestion found for '{ingredient}'"}, status_code=404)

# Example usage:
# GET /suggestions                -> returns all swap suggestions
# GET /suggestion?ingredient=Olive oil   -> returns swap suggestion for "Olive oil"

# To run:
#   uvicorn ingredient_suggestion_api:app --reload
