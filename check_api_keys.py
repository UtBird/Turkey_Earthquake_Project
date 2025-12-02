import requests
import json

API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
response = requests.get(API_URL)
data = response.json()
if data["result"]:
    print(data["result"][0].keys())
    print(data["result"][0])
