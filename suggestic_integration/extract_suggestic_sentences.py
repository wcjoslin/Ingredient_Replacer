import json
from suggestic_integration.suggestic_api import query_suggestic

def fetch_ingredient_sentences(ingredient, output_path):
    query = f'''
    {{
      searchRecipesByIngredients(
        mustIngredients: ["{ingredient}"]
      ) {{
        edges {{
          node {{
            name
            ingredientLines
            instructions
          }}
        }}
      }}
    }}
    '''
    response = query_suggestic(query)
    recipes = response.get("data", {}).get("searchRecipesByIngredients", {}).get("edges", [])
    sentences = []
    for recipe in recipes:
        lines = recipe["node"].get("ingredientLines", [])
        for line in lines:
            if ingredient.lower() in line.lower():
                sentences.append(line)
        # Also extract from instructions if present
        instructions = recipe["node"].get("instructions", [])
        if isinstance(instructions, list):
            for instr_line in instructions:
                if ingredient.lower() in instr_line.lower():
                    sentences.append(instr_line)
        elif isinstance(instructions, str):
            for instr_line in instructions.split("\n"):
                if ingredient.lower() in instr_line.lower():
                    sentences.append(instr_line)
    with open(output_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")
    print(f"Extracted {len(sentences)} sentences for '{ingredient}' to {output_path}")

if __name__ == "__main__":
    fetch_ingredient_sentences("olive oil", "suggestic_ingredient_sentences_olive_oil.txt")
