import pytest
import httpx

# Assumes FastAPI is running locally on port 8000

@pytest.fixture(scope="module")
def api_url():
    return "http://127.0.0.1:8000/suggestions"

def test_suggestions_valid_payload(api_url):
    payload = {
        "ingredients": [
            "¾ cup parmesan cheese",
            "egg",
            "mozzarella cheese",
            "olive oil"
        ],
        "diets": ["vegan"]
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    # Should flag eggs and cheese for vegan
    flagged = [s["original"] for s in data["suggestions"]]
    assert any("egg" in f or "cheese" in f for f in flagged)

def test_suggestions_empty_ingredients(api_url):
    payload = {
        "ingredients": [],
        "diets": ["vegan"]
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert data["suggestions"] == []

def test_suggestions_no_diets(api_url):
    payload = {
        "ingredients": [
            "egg",
            "mozzarella cheese"
        ]
        # No diets
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    # Should be empty since no restrictions
    assert data["suggestions"] == []

def test_suggestions_unknown_ingredient(api_url):
    payload = {
        "ingredients": [
            "unknown ingredient"
        ],
        "diets": ["vegan"]
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    # Should be empty since ingredient is not mapped
    assert data["suggestions"] == []

def test_suggestions_malformed_payload(api_url):
    # Missing 'ingredients' key
    payload = {
        "diets": ["vegan"]
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data

def test_suggestions_large_ingredient_list(api_url):
    payload = {
        "ingredients": ["egg"] * 100,
        "diets": ["vegan"]
    }
    response = httpx.post(api_url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    # Should flag many eggs for vegan
    assert len(data["suggestions"]) > 0
