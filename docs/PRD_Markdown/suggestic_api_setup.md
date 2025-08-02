# Suggestic API Setup

## 1. Register for API Access

- Visit [Suggestic API](https://suggestic.com/) and sign up for an account.
- Request API access and obtain your API key from the Suggestic developer portal.

## 2. Store Your API Key

- Open the `config.py` file in your project root.
- Replace the placeholder value for `SUGGESTIC_API_KEY` with your actual API key:
  ```python
  SUGGESTIC_API_KEY = "your_actual_api_key_here"
  ```
- Save the file.
- **Do not commit your real API key to public version control.** If sharing code, use a placeholder value.

## 3. Basic API Usage

- Use the provided `suggestic_api.py` module to authenticate and make requests.

### Example Usage

```python
from suggestic_api import query_suggestic

# Example: Get list of meal plans
query = """
{
  mealPlans {
    id
    name
  }
}
"""
result = query_suggestic(query)
print(result)
```

- Ensure your `config.py` contains:
  ```python
  SUGGESTIC_API_URL = "https://api.suggestic.com/graphql"
  SUGGESTIC_API_KEY = "your_api_key_here"
  ```
