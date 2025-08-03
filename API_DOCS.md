# Ingredient Replacer API Documentation

## Overview

This API powers the Ingredient Replacer App, providing endpoints for:
- FDA-style nutrition label generation
- Ingredient swap suggestions (foodBERT-powered, cache-based)
- Ingredient enrichment and dietary restriction analysis

---

## Endpoints

### 1. POST `/nutrition-label` (Flask API)

**Description:**  
Generate a nutrition label image and nutrition summary for a recipe.

**Request:**
```json
{
  "ingredients": [
    {"name": "all purpose flour", "amount": "2 cups"},
    {"name": "almond milk", "amount": "1 cup"},
    "egg"
  ],
  "servings": 4
}
```

**Response:**
```json
{
  "nutrition_label_image": "<base64 PNG>",
  "nutrition_summary": { ... }
}
```

---

### 2. POST `/suggestions` (FastAPI)

**Description:**  
Suggest ingredient swaps for flagged ingredients, using a precomputed foodBERT cache.

**Request:**
```json
{
  "ingredients": ["egg", "milk"],
  "diets": ["keto", "vegan"]
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "original": "egg",
      "categories": [...],
      "display_categories": [...],
      "dietary_flags": [...],
      "swap_suggestion": {
        "ranked_swaps": [
          {"substitute": "tofu", "score": 0.92, ...}
        ]
      }
    }
  ]
}
```

**Performance:**  
Swap suggestions are instant, using the cache at `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`.

---

### 3. POST `/enrich_ingredients` (FastAPI)

**Description:**  
Enrich ingredient data for UI display (nutrition, categories, dietary flags).

**Request:**
```json
{
  "ingredients": ["egg", "milk"]
}
```

**Response:**
```json
{
  "ingredients": [
    {
      "ingredient": "egg",
      "nutrition": { ... },
      "categories": [...],
      "display_categories": [...],
      "dietary_flags": [...]
    }
  ]
}
```

---

## Regenerating the foodBERT Swap Cache

If you add new ingredients or want to refresh swap suggestions:
1. Run: `python foodBERT/foodbert_embeddings/precompute_foodbert_swaps.py`
2. This will regenerate `foodBERT/foodbert_embeddings/foodbert_swap_cache.json`
3. Restart the backend API to load the new cache

---

## Requirements

- Python 3.10+ (backend)
- Node.js 18+ (frontend)
- Flask, flask-cors, FastAPI, uvicorn, Pillow, pytest

---

## Changelog

**2025-08-03**
- Ingredient swap suggestions now use a precomputed cache for speed and reliability.
- Documentation updated for new endpoints and cache workflow.
- Nutrition label API and swap suggestion API usage clarified.
