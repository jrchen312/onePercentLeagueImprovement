#gets the champion stats upone entering a champion name. 
#
# Does not require an API
#
import requests
import json
import random

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



#that's nice, but can we get more information?
championName = "Aatrox"
championLink = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion/' + championName + '.json'

championData = requests.get(championLink)
#print(championData.json()['data'][championName])

stuff = []
for key in championData.json()['data'][championName]:
    stuff.append(key)
print(stuff)


"""
#chioces:
# ['id', 'key', 'name', 'title', 'image', 'skins', 'lore', 'blurb', 'allytips', 'enemytips', 'tags', 'partype', 'info', 'stats', 'spells', 'passive', 'recommended']
print(championData.json()['data'][championName]['id']) #aatrox+
print(championData.json()['data'][championName]['key']) #206
print(championData.json()['data'][championName]['name']) #aatrox
print(championData.json()['data'][championName]['title']) #the Darkin Blade+
print(championData.json()['data'][championName]['image']) #image is useless imo
print(championData.json()['data'][championName]['skins']) #get the numbers of each skin+
print(championData.json()['data'][championName]['lore']) #lore+
print(championData.json()['data'][championName]['blurb']) #blurb
print(championData.json()['data'][championName]['allytips']) #+
print(championData.json()['data'][championName]['enemytips'])
print(championData.json()['data'][championName]['tags']) #fighter, tank+
print(championData.json()['data'][championName]['partype'])# ?? "Blood Well"
print(championData.json()['data'][championName]['info']) #??, difficulty
print(championData.json()['data'][championName]['stats']) #base stats, stats per level, +
jprint(championData.json()['data'][championName]['spells']) #needs more analysis
print(championData.json()['data'][championName]['passive']) #passive
print(championData.json()['data'][championName]['recommended']) #? useless??
"""

while True:
    championName = input("Champion Name: ").title().strip()
    # ISSUE: doesn't work for lee sin.
    i = championName.find(" ")
    while i != -1:
        championName = championName[0:i] + championName[i+1:] 
        i = championName.find(" ")

    if championName not in championDicts:
        print("Name not in database, try again. ")
        continue
    print("searching.... hold on")

    #creates an API link based on the lastestVersion global variable and the championName that the user inputted. 
    championLink = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion/' + championName + '.json'

    championData = requests.get(championLink)
    if (championData.status_code) != 200:
        print("Something is wrong, please try again.")
        continue

    championName = championData.json()['data'][championName]['id']
    championTitle = championData.json()['data'][championName]['title']

    championSkinDict = championData.json()['data'][championName]['skins']
    championSkinNums = []
    for dictionary in championSkinDict:
        championSkinNums.append(dictionary['num'])
    
    championLore = championData.json()['data'][championName]['lore']

    try:
        championTip = random.choice(championData.json()['data'][championName]['allytips'])
    except:
        championTip = "Nvm, don't have one XD"
    

    championAttributesList = championData.json()['data'][championName]['tags']
    championAttributes = championAttributesList[0]
    for i in range(1, len(championAttributesList)):
        championAttributes = championAttributes + "/" + championAttributesList[i]
    #print(f"{championName} is a {championAttributes}")
    
    championDifficulty = championData.json()['data'][championName]['info']['difficulty']
    #print("Champion Difficulty: " + str(championDifficulty) + "/10")

    championStats = championData.json()['data'][championName]['stats']
    #print(championStats)

    baseHP = championStats['hp']
    hpperlevel = championStats['hpperlevel']

    baseMP = championStats['mp']
    mpperlevel = championStats['mpperlevel']

    armor = championStats['armor']
    amorperlevel = championStats['armorperlevel']

    magicresist = championStats['spellblock']
    magicresisterperlevel = championStats['spellblockperlevel']

    hpregen = championStats['hpregen']
    hpregenperlevel = championStats['hpregenperlevel']

    mpregen = championStats['mpregen']
    mpregenperlevel = championStats['mpregenperlevel']

    crit = championStats['crit']
    critperlevel = championStats['critperlevel']

    attackdamage = championStats['attackdamage']
    attackdamageperlevel = championStats['attackdamageperlevel']

    attackspeed = championStats['attackspeed']
    attackspeedperlevel = championStats['attackspeedperlevel']

    movespeed = championStats['movespeed']
    attackrange = championStats['attackrange']

    level = 18

    print()
    print(championName.upper()+ ", " +championTitle.title() + ":")
    print(f"{championName} is a {championAttributes}")
    print("A tip: ", end="")
    print(championTip)
    print("Champion Difficulty: " + str(championDifficulty) + "/10")
    print()

    #delete most of this later. processing the abilities: (Q ability)
    #jprint(championData.json()['data'][championName]['spells'][0])
    q = championData.json()['data'][championName]['spells'][0]

    qAttributes = []
    for key in q:
        qAttributes.append(key)
    #print(qAttributes)

    jprint(championData.json()['data'][championName]['passive'])

    passiveImgLink = championData.json()['data'][championName]['passive']['image']['full'] #Lulu.png
    description = championData.json()['data'][championName]['passive']['description']
    passiveName = championData.json()['data'][championName]['passive']['name']


    #test = requests.get('https://cdn.communitydragon.org/latest/champion/aatrox/data')
    #print(test.status_code)