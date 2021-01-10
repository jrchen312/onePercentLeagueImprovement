#gets the champion stats upone entering a champion name. 
#
# Does not require an API
#
import requests
import json

#printing json files. 
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


#pre data processing:
versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
latestVersion = versions.json()[0]

#link: http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json
championLinks = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion.json'

championData = requests.get(championLinks)
#print(championData.json())

championDicts = championData.json()['data']
#print(championDicts)

Aatrox = championDicts['Aatrox']
#print(Aatrox)


#that's nice, but can we get more information?
championName = "Aatrox"
championLink = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion/' + championName + '.json'

championData = requests.get(championLink)
print(championData.json()['data'][championName])


