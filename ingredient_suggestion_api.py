# ingredient_suggestion_api.py
# Enhanced FastAPI endpoint to serve multi-ingredient suggestions with dietary restriction filtering and CORS support

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json

app = FastAPI(title="Multi-Ingredient Suggestion API")

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load swap suggestions at startup
with open("swap_suggestions_official.json", "r", encoding="utf-8") as f:
    SUGGESTIONS = json.load(f)

def filter_suggestions_by_diet(suggestions, diets: Optional[List[str]]):
    if not diets or len(diets) == 0:
        return suggestions
    filtered = []
    for entry in suggestions:
        # Assume each entry has a 'diets' field: list of compatible diet keys
        # If not present, treat as compatible with all diets
        entry_diets = entry.get("diets", [])
        if not entry_diets or any(diet in entry_diets for diet in diets):
            filtered.append(entry)
    return filtered

@app.get("/suggestions")
def get_all_suggestions(diets: Optional[List[str]] = Query(None, description="Dietary restriction keys")):
    """
    Return all ingredient swap suggestions, optionally filtered by dietary restrictions.
    Example: /suggestions?diets=vegan&diets=glutenfree
    """
    filtered = filter_suggestions_by_diet(SUGGESTIONS, diets)
    return JSONResponse(content=filtered)

@app.get("/suggestion")
def get_suggestion(
    ingredient: str = Query(..., description="Ingredient name to query"),
    diets: Optional[List[str]] = Query(None, description="Dietary restriction keys"),
):
    """
    Return swap suggestion for a specific ingredient, optionally filtered by dietary restrictions.
    """
    ingredient_lower = ingredient.lower().strip()
    filtered = filter_suggestions_by_diet(SUGGESTIONS, diets)
    for entry in filtered:
        if entry["ingredient"].lower().strip() == ingredient_lower:
            return JSONResponse(content=entry)
    return JSONResponse(content={"error": f"No swap suggestion found for '{ingredient}'"}, status_code=404)

# Example usage:
# GET /suggestions                -> returns all swap suggestions
# GET /suggestions?diets=vegan    -> returns vegan-compatible swaps
# GET /suggestion?ingredient=Olive oil&diets=vegan   -> returns vegan swap for "Olive oil"

# To run:
#   uvicorn ingredient_suggestion_api:app --reload
