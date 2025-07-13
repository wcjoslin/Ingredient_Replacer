import base64

SUGGESTIC_API_URL = "https://production.suggestic.com/graphql"
# The API key is base64-encoded for basic obfuscation
_OBFUSCATED_API_KEY = "OGY0NmVmMWJmNmRmYWI0ZDgwNDIxN2QxMjRlM2VhZDA4ODlhMDU1Nw=="
SUGGESTIC_API_KEY = base64.b64decode(_OBFUSCATED_API_KEY).decode()

USDA_API_KEY = "EeqMEhzym5A3UA1jpkDwP0rYDJ5R8QwKlFlkucFl"
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1"
