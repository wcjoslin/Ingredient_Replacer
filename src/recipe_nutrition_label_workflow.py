"""
Module: recipe_nutrition_label_workflow.py

Purpose:
Generate a stylized FDA-like nutrition label image from recipe nutrition data, with right-aligned numbers.

Functions:
- parse_recipe(recipe_data): Extracts ingredients and servings from a recipe dict.
- load_nutrition_data(path): Loads nutrition data from JSON.
- get_ingredient_nutrition(ingredient, nutrition_data): Retrieves nutrition profile for an ingredient.
- sum_recipe_nutrition(ingredient_list, nutrition_data, servings): Sums nutrition facts for the recipe, adjusting for servings.
- generate_fda_style_nutrition_label(nutrition_summary, output_path): Creates FDA-style nutrition label image.
- process_recipe_upload_fda_style(recipe_data, nutrition_data_path, output_image_path): Full workflow for FDA-style label.
"""

import json
from PIL import Image, ImageDraw, ImageFont

def parse_recipe(recipe_data):
    ingredients = []
    servings = recipe_data.get('servings', 1)
    raw_ingredients = recipe_data.get('ingredients', [])
    for item in raw_ingredients:
        if isinstance(item, dict) and 'name' in item:
            ingredients.append(item['name'])
        elif isinstance(item, str):
            ingredients.append(item)
    return ingredients, servings

def load_nutrition_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    nutrition_dict = {}
    for entry in data:
        ingr = entry.get("ingredient")
        profile = entry.get("nutritionix_nutrition_profile")
        if ingr and profile:
            nutrition_dict[ingr.lower().strip()] = profile
    return nutrition_dict

def get_ingredient_nutrition(ingredient, nutrition_data):
    return nutrition_data.get(ingredient.lower().strip())

def sum_recipe_nutrition(ingredient_list, nutrition_data, servings=1):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0}
    for ingr in ingredient_list:
        profile = get_ingredient_nutrition(ingr, nutrition_data)
        if profile:
            for key in total:
                total[key] += profile.get(key, 0)
    per_serving = {k: v / servings for k, v in total.items()}
    return {"total": total, "per_serving": per_serving}

def right_align_text(draw, text, y, font, right_margin=30, image_width=400):
    text_width, _ = draw.textsize(text, font=font)
    x = image_width - right_margin - text_width
    draw.text((x, y), text, fill="black", font=font)

def generate_fda_style_nutrition_label(nutrition_summary, output_path):
    """
    Generates a stylized FDA-like nutrition label image with right-aligned numbers.
    """
    width, height = 400, 500
    bg_color = "white"
    text_color = "black"
    bold_font_size = 36
    header_font_size = 28
    regular_font_size = 22
    small_font_size = 16

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        bold_font = ImageFont.truetype("arialbd.ttf", bold_font_size)
        header_font = ImageFont.truetype("arialbd.ttf", header_font_size)
        regular_font = ImageFont.truetype("arial.ttf", regular_font_size)
        small_font = ImageFont.truetype("arial.ttf", small_font_size)
    except:
        bold_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw outer border
    draw.rectangle([10, 10, width-10, height-10], outline="black", width=6)

    y = 25
    # Nutrition Facts header
    draw.text((25, y), "Nutrition Facts", fill=text_color, font=bold_font)
    y += bold_font_size + 10

    # Thick line
    draw.line([(15, y), (width-15, y)], fill="black", width=6)
    y += 15

    # Serving Size
    draw.text((25, y), "Serving Size: 1 serving", fill=text_color, font=regular_font)
    y += regular_font_size + 5

    # Calories section
    draw.text((25, y), "Calories", fill=text_color, font=header_font)
    right_align_text(draw, f"{nutrition_summary['per_serving']['calories']:.0f}", y, header_font, right_margin=30, image_width=width)
    y += header_font_size + 8

    # Thin line
    draw.line([(15, y), (width-15, y)], fill="black", width=2)
    y += 10

    # Nutrients
    draw.text((25, y), "Total Fat", fill=text_color, font=regular_font)
    right_align_text(draw, f"{nutrition_summary['per_serving']['fat']:.1f}g", y, regular_font, right_margin=30, image_width=width)
    y += regular_font_size + 2

    draw.text((25, y), "Protein", fill=text_color, font=regular_font)
    right_align_text(draw, f"{nutrition_summary['per_serving']['protein']:.1f}g", y, regular_font, right_margin=30, image_width=width)
    y += regular_font_size + 2

    draw.text((25, y), "Total Carbohydrate", fill=text_color, font=regular_font)
    right_align_text(draw, f"{nutrition_summary['per_serving']['carbohydrates']:.1f}g", y, regular_font, right_margin=30, image_width=width)
    y += regular_font_size + 2

    # Thin line
    y += 8
    draw.line([(15, y), (width-15, y)], fill="black", width=2)
    y += 10

    # Footer
    draw.text((25, y), "Not a significant source of other nutrients.", fill=text_color, font=small_font)

    img.save(output_path)

def process_recipe_upload_fda_style(recipe_data, nutrition_data_path, output_image_path):
    ingr_list, servings = parse_recipe(recipe_data)
    nutrition_data = load_nutrition_data(nutrition_data_path)
    nutrition_summary = sum_recipe_nutrition(ingr_list, nutrition_data, servings)
    generate_fda_style_nutrition_label(nutrition_summary, output_image_path)
    return nutrition_summary

# Example usage
if __name__ == "__main__":
    sample_recipe = {
        "ingredients": [
            {"name": "all purpose flour", "amount": "2 cups"},
            {"name": "almond milk", "amount": "1 cup"},
            "egg"
        ],
        "servings": 4
    }
    nutrition_summary = process_recipe_upload_fda_style(
        sample_recipe,
        "data enrichment/enriched_ingredient_data_nutritionix.json",
        "nutrition_label_fda_style.png"
    )
    print("Nutrition Summary:", nutrition_summary)
