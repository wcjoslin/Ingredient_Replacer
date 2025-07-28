# Ingredient Replacer API Documentation

## Overview

This API provides ingredient swap suggestions based on user-provided ingredients and dietary restrictions, powered by foodBERT and custom logic.

---

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### POST `/suggestions`

**Description:**  
Get swap suggestions for a list of ingredients, optionally filtered by dietary restrictions.

**Request Body (JSON):**
```json
{
  "ingredients": ["ingredient1", "ingredient2", "..."],
  "diets": ["vegan", "glutenfree", "..."] // optional
}
```

- `ingredients`: (array of strings) List of ingredient names.
- `diets`: (optional, array of strings) List of dietary restriction IDs.

**Response (200 OK):**
```json
{
  "suggestions": [
    {
      "original": "ingredient1",
      "swap_suggestion": {
        // swap suggestion details (structure depends on backend logic)
      }
    },
    ...
  ]
}
```

**Error Responses:**
- `405 Method Not Allowed`: If using GET on `/suggestions`.
- `422 Unprocessable Entity`: If request body is invalid.

---

## Example Usage

### Request

```http
POST /suggestions HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "ingredients": ["egg", "milk", "flour"],
  "diets": ["vegan"]
}
```

### Response

```json
{
  "suggestions": [
    {
      "original": "egg",
      "swap_suggestion": {
        "swap": "flaxseed meal",
        "score": 0.92,
        "reason": "Vegan alternative"
      }
    },
    ...
  ]
}
```

---

## Notes

- The `/suggestions` endpoint expects a JSON body.
- The list of supported `diets` can be found in your `dietary_restriction_presets.json`.
- The structure of `swap_suggestion` may include fields like `swap`, `score`, and `reason`, depending on your backend implementation.

---

## Contact

For questions or issues, please open an issue on GitHub or contact the project maintainer.
