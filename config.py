import base64

SUGGESTIC_API_URL = "https://production.suggestic.com/graphql"
import os
# Load API keys from environment variables
SUGGESTIC_API_KEY = os.environ.get("SUGGESTIC_API_KEY")

USDA_API_KEY = os.environ.get("USDA_API_KEY")
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1"

# Ingredient suggestion configuration
INGREDIENT_SUGGESTION_SCORE_THRESHOLD = 0.48  # Minimum confidence score for suggestions
INGREDIENT_SUGGESTION_ALLOWED_CATEGORIES = [
    "vegetable", "fruit", "protein", "grain", "dairy", "spice", "condiment"
]  # Example categories, update as needed
