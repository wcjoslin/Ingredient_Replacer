import requests
from config import SUGGESTIC_API_URL, SUGGESTIC_API_KEY

def query_suggestic(query: str, variables: dict = {}):
    headers = {
        "Authorization": f"Token {SUGGESTIC_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": query, "variables": variables}
    response = requests.post(SUGGESTIC_API_URL, json=payload, headers=headers)
    return response.json()

