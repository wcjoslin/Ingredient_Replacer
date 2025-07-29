"""
API endpoint for generating FDA-style nutrition label images for uploaded recipes.

POST /nutrition-label
Request JSON:
{
    "ingredients": [
        {"name": "all purpose flour", "amount": "2 cups"},
        {"name": "almond milk", "amount": "1 cup"},
        "egg"
    ],
    "servings": 4
}

Response JSON:
{
    "nutrition_label_image": "<base64-encoded PNG>",
    "nutrition_summary": {...}
}
"""

import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from recipe_nutrition_label_workflow import process_recipe_upload_fda_style

app = Flask(__name__)
CORS(app)

@app.route("/nutrition-label", methods=["POST"])
def nutrition_label():
    data = request.get_json()
    recipe_data = {
        "ingredients": data.get("ingredients", []),
        "servings": data.get("servings", 1)
    }
    # Generate nutrition label image
    nutrition_summary = process_recipe_upload_fda_style(
        recipe_data,
        "data enrichment/enriched_ingredient_data_nutritionix.json",
        "nutrition_label_fda_style.png"
    )
    # Encode image as base64
    with open("nutrition_label_fda_style.png", "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return jsonify({
        "nutrition_label_image": img_b64,
        "nutrition_summary": nutrition_summary
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True)
