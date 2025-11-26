import requests
import json

API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
response = requests.get(API_URL)
data = response.json()
print(json.dumps(data["result"][:3], indent=2))
