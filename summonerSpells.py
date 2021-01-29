import json
import requests

#printing json files. 
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


"""
versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
latestVersion = versions.json()[0]

url = 'https://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/summoner.json'

summonerSpellInfo = requests.get(url).json()['data']
print(summonerSpellInfo)

#the goal is to get a dictionary with:
#       [str(spell1Id)] -> 'id'
#             'key' (21) -> 'id' ('SummonerBarrier')
spellkeyToId = dict()
for spellName in summonerSpellInfo:
    print(spellName)
    spellkeyToId[summonerSpellInfo[spellName]['key']] = summonerSpellInfo[spellName]['id'] + '.png'

print(spellkeyToId)#

useThis = {'21': 'SummonerBarrier.png', '1': 'SummonerBoost.png', '14': 'SummonerDot.png', 
'3': 'SummonerExhaust.png', '4': 'SummonerFlash.png', '6': 'SummonerHaste.png', 
'7': 'SummonerHeal.png', '13': 'SummonerMana.png', '30': 'SummonerPoroRecall.png', 
'31': 'SummonerPoroThrow.png', '11': 'SummonerSmite.png', '39': 'SummonerSnowURFSnowball_Mark.png', 
'32': 'SummonerSnowball.png', '12': 'SummonerTeleport.png'}   
print(useThis)
"""

gameModes = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
gameModes = gameModes.json()

queueToDescription = dict()
for dictionary in gameModes:
    description = dictionary['description']
    if description == None:
        description = "Custom games"
    index = description.find(' games')
    if index >= 0:
        description = description[:index]
    index = description.find('5v5 ')
    if index >= 0:
        description = description[index+4:]
    queueToDescription[dictionary['queueId']] = description


jprint(queueToDescription)