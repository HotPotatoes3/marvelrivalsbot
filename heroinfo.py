import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
MR_KEY = os.getenv('MR_KEY')
headers = {
        'X-API-Key': MR_KEY,
    }

def getbasicInfo(name):

    try:
        response = requests.get(f'https://mrapi.org/api/player-id/{name}', headers=headers)
        data = response.json()
        
        requests.get(f'https://mrapi.org/api/player-update/{data["id"]}', headers=headers)   
        
        info = requests.get(f'https://mrapi.org/api/player/{data["id"]}', headers=headers)    
        
        playerinfo = info.json()
        return playerinfo
    except Exception as e:
        return "An error has occured"
    

def getPic(id):
    response = requests.get(f'https://mrapi.org/api/item/{id}', headers=headers)
    return response.json()['icon']
        
    