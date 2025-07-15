import json
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from suggestic_api import query_suggestic
from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict
from foodBERT.foodbert_embeddings.helpers.approx_knn_classifier import ApproxKNNClassifier

def suggestic_foodbert_ingredient_swap(
    recipe_id,
    output_json_path="ingredient_swap_result.json",
    error_log_path="ingredient_swap_errors.json"
):
    """
    Query a Suggestic recipe by ID, extract the first ingredient, and use foodBERT to suggest a substitute.
    Outputs results as JSON and logs missing ingredients.
    """
    # Step 1: Query Suggestic API for recipe
    query = f'''
    {{
      recipe(id: "{recipe_id}") {{
        databaseId
        name
        ingredients {{
          name
        }}
      }}
    }}
    '''
    print("DEBUG: Querying Suggestic API...")
    response = query_suggestic(query)
    print("DEBUG: API response:", response)
    recipe = response.get("data", {}).get("recipe", {})
    recipe_name = recipe.get("name", "")
    ingredients = [i["name"].strip().lower() for i in recipe.get("ingredients", [])]
    print("DEBUG: Extracted ingredients:", ingredients)

    result = {
        "recipe_id": recipe_id,
        "recipe_name": recipe_name,
        "original_ingredient": None,
        "substitute": None,
        "score": None,
        "all_ingredients": ingredients
    }
    errors = []

    if not ingredients:
        print("ERROR: No ingredients found in recipe.")
        errors.append({
            "error": "No ingredients found",
            "recipe_id": recipe_id,
            "recipe_name": recipe_name
        })
    else:
        # Step 2: Get first ingredient
        ingredient = ingredients[0]
        result["original_ingredient"] = ingredient

        # Step 3: Load foodBERT embeddings
        embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
        if ingredient not in embedding_dict:
            print(f"ERROR: Ingredient '{ingredient}' not in embedding vocabulary.")
            errors.append({
                "error": "Ingredient not in embedding vocabulary",
                "ingredient": ingredient,
                "recipe_id": recipe_id,
                "recipe_name": recipe_name,
                "all_ingredients": ingredients
            })
        else:
            # Step 4: Find substitute using ApproxKNNClassifier
            all_ingredient_embeddings = []
            all_ingredient_labels = []
            for key, value in embedding_dict.items():
                all_ingredient_embeddings.append(value)
                all_ingredient_labels.extend([key] * len(value))
            import numpy as np
            all_ingredient_embeddings = np.concatenate(all_ingredient_embeddings)
            all_ingredient_labels = np.stack(all_ingredient_labels)
            knn = ApproxKNNClassifier(all_ingredient_embeddings=all_ingredient_embeddings, max_embedding_count=100)
            ingredient_embeddings = embedding_dict[ingredient]
            distances, indices = knn.k_nearest_neighbors(ingredient_embeddings)
            # Flatten and get best substitute (excluding self)
            flat_indices = indices.flatten()
            flat_distances = distances.flatten()
            best_idx = None
            for idx, label in zip(flat_indices, all_ingredient_labels[flat_indices]):
                if label != ingredient:
                    best_idx = idx
                    break
            if best_idx is not None:
                substitute = all_ingredient_labels[best_idx]
                score = float(flat_distances[list(flat_indices).index(best_idx)])
                print(f"DEBUG: Substitute for '{ingredient}' is '{substitute}' with score {score}")
                result["substitute"] = substitute
                result["score"] = score
            else:
                print(f"ERROR: No substitute found for '{ingredient}'")
                errors.append({
                    "error": "No substitute found",
                    "ingredient": ingredient,
                    "recipe_id": recipe_id,
                    "recipe_name": recipe_name
                })

    # Step 5: Output results
    print("DEBUG: Writing result to", output_json_path)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    if errors:
        print("DEBUG: Writing errors to", error_log_path)
        with open(error_log_path, "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
