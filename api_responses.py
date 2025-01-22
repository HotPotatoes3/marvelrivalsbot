import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv('API_KEY')


headers = {
    "Accept": "application/json",
    "apikey": f"{API_KEY}",
    "accept": "application/json",
}

def propertyCall(address, zipcode):
    response = requests.get(f"https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/basicprofile?address1={address}&address2={zipcode}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return response.json()