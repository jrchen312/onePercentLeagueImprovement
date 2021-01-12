#apparently ddragon sucks dick (true)

endpoints = ["https://cdn.communitydragon.org/:patch/champion/generic/square","https://cdn.communitydragon.org/:patch/champion/:championKey/square","https://cdn.communitydragon.org/:patch/champion/:championId/square","https://cdn.communitydragon.org/:patch/champion/:championKey/data","https://cdn.communitydragon.org/:patch/champion/:championId/data","https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art","https://cdn.communitydragon.org/:patch/champion/:championId/splash-art","https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/centered","https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/centered","https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/centered/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/centered/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/ban","https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/ban","https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/choose","https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/choose","https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/sfx","https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/sfx","https://cdn.communitydragon.org/:patch/champion/:championKey/tile","https://cdn.communitydragon.org/:patch/champion/:championId/tile","https://cdn.communitydragon.org/:patch/champion/:championKey/tile/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championId/tile/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championKey/portrait","https://cdn.communitydragon.org/:patch/champion/:championId/portrait","https://cdn.communitydragon.org/:patch/champion/:championKey/portrait/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championId/portrait/skin/:skinId","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/passive","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/passive","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/p","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/p","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/q","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/q","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/w","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/w","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/e","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/e","https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/r","https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/r","https://cdn.communitydragon.org/:patch/honor/generic","https://cdn.communitydragon.org/:patch/honor/:honorId","https://cdn.communitydragon.org/:patch/honor/:honorId/locked","https://cdn.communitydragon.org/:patch/honor/:honorId/level/:level","https://cdn.communitydragon.org/:patch/honor/emblem/generic","https://cdn.communitydragon.org/:patch/honor/emblem/:honorId","https://cdn.communitydragon.org/:patch/honor/emblem/:honorId/locked","https://cdn.communitydragon.org/:patch/honor/emblem/:honorId/level/:level","https://cdn.communitydragon.org/:patch/ward/:wardId","https://cdn.communitydragon.org/:patch/ward/:wardId/shadow","https://cdn.communitydragon.org/:patch/profile-icon/:profileIconId"]
endpointList = ""
for endpoint in endpoints:
    endpointList = endpointList + '\n' + endpoint

#print(endpointList) 

"""
enpoints:
https://cdn.communitydragon.org/:patch/champion/generic/square     
https://cdn.communitydragon.org/:patch/champion/:championKey/square
https://cdn.communitydragon.org/:patch/champion/:championId/square 
https://cdn.communitydragon.org/:patch/champion/:championKey/data  
https://cdn.communitydragon.org/:patch/champion/:championId/data
https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art
https://cdn.communitydragon.org/:patch/champion/:championId/splash-art
https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/centered
https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/centered
https://cdn.communitydragon.org/:patch/champion/:championKey/splash-art/centered/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championId/splash-art/centered/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/ban
https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/ban
https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/choose
https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/choose
https://cdn.communitydragon.org/:patch/champion/:championKey/champ-select/sounds/sfx
https://cdn.communitydragon.org/:patch/champion/:championId/champ-select/sounds/sfx
https://cdn.communitydragon.org/:patch/champion/:championKey/tile
https://cdn.communitydragon.org/:patch/champion/:championId/tile
https://cdn.communitydragon.org/:patch/champion/:championKey/tile/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championId/tile/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championKey/portrait
https://cdn.communitydragon.org/:patch/champion/:championId/portrait
https://cdn.communitydragon.org/:patch/champion/:championKey/portrait/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championId/portrait/skin/:skinId
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/passive
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/passive
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/p
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/p
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/q
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/q
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/w
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/w
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/e
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/e
https://cdn.communitydragon.org/:patch/champion/:championKey/ability-icon/r
https://cdn.communitydragon.org/:patch/champion/:championId/ability-icon/r
https://cdn.communitydragon.org/:patch/honor/generic
https://cdn.communitydragon.org/:patch/honor/:honorId
https://cdn.communitydragon.org/:patch/honor/:honorId/locked
https://cdn.communitydragon.org/:patch/honor/:honorId/level/:level
https://cdn.communitydragon.org/:patch/honor/emblem/generic
https://cdn.communitydragon.org/:patch/honor/emblem/:honorId
https://cdn.communitydragon.org/:patch/honor/emblem/:honorId/locked
https://cdn.communitydragon.org/:patch/honor/emblem/:honorId/level/:level
https://cdn.communitydragon.org/:patch/ward/:wardId
https://cdn.communitydragon.org/:patch/ward/:wardId/shadow
https://cdn.communitydragon.org/:patch/profile-icon/:profileIconId

"""

"""
# download the latest patch
python3 -m cdragontoolbox download patch=11.1

# locate champion bin files 
# note: the `*` directory is a version, it changes
ls RADS/projects/lol_game_client/releases/*/files/DATA/FINAL/Champions/*.wad.client

# extract bin file for the champion from the .wad.client file
# the bin file is named `data/characters/<name>/<name>.bin`
# here, we will extract Janna's bin file
python3 -m cdragontoolbox wad-extract -uno -p data/characters/janna/janna.bin RADS/projects/lol_game_client/releases/*/files/DATA/FINAL/Champions/Janna.wad.client

# dump the bin data into text form
python3 -m cdragontoolbox bin-dump data/characters/janna/janna.bin
"""
import requests
import json

#printing json files. 
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


help = requests.get('https://raw.communitydragon.org/pbe/game/data/characters/aatrox/aatrox.bin.json')
print(help.status_code)

print()
jprint(help.json()['Characters/Aatrox/Spells/AatroxQ'])

d = []
for f in help.json():
    d.append(f)
print(d)





yone = requests.get('http://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/777.json')
#jprint(yone.json())

contents = []
for key in yone.json():
    contents.append(key)
#print(contents)