import requests
import json


response = requests.get("http://api.open-notify.org/astros.json")
print(response.status_code)

# response.json() is a dictionary. 
print(response.json())

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())
print()




#obtaining the names of each person on the ISS right now:
print(type(response.json()))
for key in response.json():
    print(key)

#list of dictionaries. 
print(response.json()['people'])

names = []
for dictionary in response.json()['people']:
    names.append(dictionary['name'])
print(names)



parameters = {
    "lat": 40.71,
    "lon": -74
}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

jprint(response.json())


"""
RGAPI-ed254041-105a-4d1e-b3c2-60fe367dd8bd

"""

print()
riotAPI = 'RGAPI-ed254041-105a-4d1e-b3c2-60fe367dd8bd'
#response = requests.get("http://na1.api.riotgames.com/RGAPI-ed254041-105a-4d1e-b3c2-60fe367dd8bd")
#print(response)


resposne = requests.get('https://na1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=' + riotAPI)
print(resposne.json())

"""
bloojayz = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/bloojayz?api_key=' + riotAPI)
print(bloojayz.json())

puuid = bloojayz.json()['puuid']
encryptedSummonerID = bloojayz.json()['id']
print(puuid)

seasonIDs = requests.get('http://static.developer.riotgames.com/docs/lol/seasons.json')
print(seasonIDs.json())
"""

hulksmash = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/hulksmash1337?api_key=' + riotAPI)
print(hulksmash.json())


awefjiiojwefjioawefjiowfjioawefjijioawejioawejioawefjiowfjiojioawef = requests.get('https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/3736067752?api_key=RGAPI-ed254041-105a-4d1e-b3c2-60fe367dd8bd')
jprint(awefjiiojwefjioawefjiowfjioawefjijioawejioawejioawefjiowfjiojioawef.json())

kimmerty = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/kimmerty?api_key=' + riotAPI)
print(kimmerty.json())