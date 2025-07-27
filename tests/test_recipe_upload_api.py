import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure the parent directory is in the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from ingredient_suggestion_api import app

client = TestClient(app)

def test_suggestions_success():
    payload = {
        "ingredients": ["egg", "milk", "flour"],
        "diets": ["vegan"]
    }
    response = client.post("/suggestions", json=payload)
    assert response.status_code == 200
    assert "suggestions" in response.json()

def test_suggestions_missing_ingredients():
    payload = {
        "diets": ["vegan"]
    }
    response = client.post("/suggestions", json=payload)
    assert response.status_code == 200
    assert "suggestions" in response.json()

def test_suggestions_invalid_method():
    response = client.get("/suggestions")
    assert response.status_code == 405
    assert "error" in response.json()
