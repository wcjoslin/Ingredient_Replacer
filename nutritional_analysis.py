import numpy as np

def calculate_nutrition_delta(profile1, profile2):
    """
    Calculates the nutritional delta between two ingredient profiles.
    A lower score indicates a smaller nutritional difference.
    """
    if not profile1 or not profile2:
        return float('inf')  # Return a large number if one of the profiles is missing

    nutrients = ["calories", "protein", "fat", "carbohydrates"]
    
    # Replace None with 0 for calculation
    p1 = np.array([profile1.get(n, 0) or 0 for n in nutrients])
    p2 = np.array([profile2.get(n, 0) or 0 for n in nutrients])

    # Normalize by the first profile's values to get a relative difference
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        delta = np.sum(np.abs(p1 - p2) / (p1 + 1e-6))
    
    return delta

if __name__ == '__main__':
    # Example Usage
    profile_a = {"calories": 100, "protein": 10, "fat": 5, "carbohydrates": 12}
    profile_b = {"calories": 110, "protein": 9, "fat": 6, "carbohydrates": 10}
    profile_c = {"calories": 200, "protein": 2, "fat": 1, "carbohydrates": 40}

    delta_ab = calculate_nutrition_delta(profile_a, profile_b)
    delta_ac = calculate_nutrition_delta(profile_a, profile_c)
    
    print(f"Nutritional Delta (A vs B): {delta_ab:.2f}")
    print(f"Nutritional Delta (A vs C): {delta_ac:.2f}")
    # Expected: Delta (A vs B) should be much smaller than Delta (A vs C)
