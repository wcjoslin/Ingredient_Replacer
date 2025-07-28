import pytest
import sys
import os

# Ensure import from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from ingredient_suggestion_api import app

client = TestClient(app)

def test_enrich_ingredients_api_full_data():
    payload = {"ingredients": ["Egg", "Milk"]}
    response = client.post("/api/enrich_ingredients", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "enriched_ingredients" in data
    assert len(data["enriched_ingredients"]) == 2
    for ingr in data["enriched_ingredients"]:
        assert "ingredient" in ingr
        assert "bullet_points" in ingr
        assert isinstance(ingr["bullet_points"], list)
        # Should have nutrition and category info for known ingredients
        if ingr["ingredient"].lower() in ["egg", "milk"]:
            assert any("Calories" in b for b in ingr["bullet_points"])

def test_enrich_ingredients_api_partial_data():
    payload = {"ingredients": ["Flour"]}
    response = client.post("/api/enrich_ingredients", json=payload)
    assert response.status_code == 200
    data = response.json()
    ingr = data["enriched_ingredients"][0]
    assert ingr["ingredient"].lower() == "flour"
    # Should have at least category or dietary info, but may lack nutrition
    assert any("Category" in b or "Not" in b or "-friendly" in b for b in ingr["bullet_points"])

def test_enrich_ingredients_api_missing_data():
    payload = {"ingredients": ["Unknown Ingredient"]}
    response = client.post("/api/enrich_ingredients", json=payload)
    assert response.status_code == 200
    data = response.json()
    ingr = data["enriched_ingredients"][0]
    assert ingr["ingredient"] == "Unknown Ingredient"
    assert any("Nutritional Information for Unknown Ingredient is incomplete" in b for b in ingr["bullet_points"])

def test_enrich_ingredients_api_empty_list():
    payload = {"ingredients": []}
    response = client.post("/api/enrich_ingredients", json=payload)
    assert response.status_code == 400
    assert "No ingredients provided" in response.text

# def test_enrich_ingredients_api_multiple_flags():
#     # This test assumes the enrichment logic and reference files are set up so that
#     # "Egg" or another ingredient matches multiple dietary restrictions.
#     payload = {"ingredients": ["Egg"]}
#     response = client.post("/api/enrich_ingredients", json=payload)
#     assert response.status_code == 200
#     data = response.json()
#     ingr = data["enriched_ingredients"][0]
#     # Should show multiple dietary flags if applicable
#     assert any("Not vegan" in b for b in ingr["bullet_points"]) or any("-friendly" in b for b in ingr["bullet_points"])

if __name__ == "__main__":
    pytest.main([__file__])
