import requests

OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product"

def get_product_metadata(ingredient_name):
    # Search for the ingredient in Open Food Facts
    search_url = f"https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": ingredient_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    data = response.json()
    products = data.get("products", [])
    if not products:
        return None
    product = products[0]
    # Extract relevant metadata tags
    metadata = {
        "vegan": product.get("ingredients_analysis_tags", []),
        "allergens": product.get("allergens_tags", []),
        "labels": product.get("labels_tags", []),
        "categories": product.get("categories_tags", [])
    }
    return metadata
