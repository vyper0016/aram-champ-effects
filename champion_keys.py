import requests
import json


def getLatestDDragon():
    versions_response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    versions = versions_response.json()
    latest = versions[0]
    ddragon_response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json")
    ddragon = ddragon_response.json()
    champions = ddragon["data"]

    with open('ddragon.json', 'w') as f:
        json.dump(champions, f, indent=3)


def getChampionByKey(key):
    with open('ddragon.json', 'r') as f:
        champions = json.load(f)

    for _, championData in champions.items():
        if int(championData["key"]) == int(key):
            return championData['name']
    return None


def getChampionById(id):
    with open('ddragon.json', 'r') as f:
        champions = json.load(f)

    for _, championData in champions.items():
        if championData["id"].upper() == id.upper():
            return championData['name']
    
    print('could not find', id)
    return None


def getChampionId(name):
    with open('ddragon.json', 'r') as f:
        champions = json.load(f)

    for _, championData in champions.items():
        if championData["name"].upper() == name.upper():
            return championData['id']
    
    print('could not find', name)
    return None

def matchId(id):
    with open('ddragon.json', 'r') as f:
        champions = json.load(f)

    for _, championData in champions.items():
        if championData["id"].upper() == id.upper():
            return championData['id']
    
    print('could not find', id)
    return None