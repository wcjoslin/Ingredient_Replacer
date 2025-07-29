import json
import base64
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nutrition_label_api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_nutrition_label_api(client):
    # Sample recipe data
    payload = {
        "ingredients": [
            "egg",
            "milk"
        ],
        "servings": 2
    }
    response = client.post("/nutrition-label", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "nutrition_label_image" in data
    assert "nutrition_summary" in data
    # Check that the image is a valid base64 PNG
    img_bytes = base64.b64decode(data["nutrition_label_image"])
    assert img_bytes[:4] == b"\x89PNG"
