# A placeholder for a more sophisticated metadata source
# In a real system, this could be populated from Open Food Facts, a database, or a detailed config file.
METADATA_CACHE = {
    "sugar": {"functional_category": "sweetener", "structural_role": "bulk"},
    "salt": {"functional_category": "seasoning", "structural_role": "flavor_enhancer"},
    "flour": {"functional_category": "flour", "structural_role": "structural"},
    "butter": {"functional_category": "fat", "structural_role": "fat"},
    "olive oil": {"functional_category": "fat", "structural_role": "fat"},
    "baking powder": {"functional_category": "leavening_agent", "structural_role": "leavening"},
    "vanilla extract": {"functional_category": "flavoring", "structural_role": "flavor_enhancer"},
    "eggs": {"functional_category": "protein", "structural_role": "structural"},
}

def get_ingredient_metadata(ingredient_name):
    """
    Retrieves metadata for a given ingredient.
    Normalizes the name for better matching.
    """
    # Simple normalization
    normalized_name = ingredient_name.lower().strip()
    return METADATA_CACHE.get(normalized_name, {})

def is_culinarily_valid(original_ingredient, substitute_ingredient):
    """
    Checks if a substitution is valid based on culinary rules.
    - Functional Category Mismatch: Prevents swapping ingredients with different core functions (e.g., fat vs. flour).
    - Structural Role Mismatch: Prevents swapping ingredients with different structural roles (e.g., structural vs. flavor enhancer).
    """
    original_meta = get_ingredient_metadata(original_ingredient)
    substitute_meta = get_ingredient_metadata(substitute_ingredient)

    # If metadata is not available, we can be lenient or strict.
    # For now, we'll be lenient and allow the swap if either is unknown.
    if not original_meta or not substitute_meta:
        return True

    # Rule 1: Functional Category Mismatch
    original_func = original_meta.get("functional_category")
    substitute_func = substitute_meta.get("functional_category")
    if original_func and substitute_func and original_func != substitute_func:
        # Allow some flexibility, e.g. fats and oils are both fats
        if "fat" in original_func and "fat" in substitute_func:
            pass
        else:
            return False # Mismatch

    # Rule 2: Structural Role Mismatch
    original_role = original_meta.get("structural_role")
    substitute_role = substitute_meta.get("structural_role")
    if original_role and substitute_role and original_role != substitute_role:
        return False # Mismatch

    return True

if __name__ == '__main__':
    # Example Usage
    print(f"Is 'sugar' for 'salt' valid? {is_culinarily_valid('sugar', 'salt')}") # Expected: False
    print(f"Is 'butter' for 'olive oil' valid? {is_culinarily_valid('butter', 'olive oil')}") # Expected: True
    print(f"Is 'flour' for 'vanilla extract' valid? {is_culinarily_valid('flour', 'vanilla extract')}") # Expected: False
    print(f"Is 'flour' for 'eggs' valid? {is_culinarily_valid('flour', 'eggs')}") # Expected: False (different functional category)
