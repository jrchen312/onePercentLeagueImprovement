#requires an API from riot

import requests
import json
from datetime import datetime
import time

API = 'RGAPI-d6e56b7d-ab94-4fd2-9583-04a04634ce82'

#printing json files. 
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def funfunsad(i, matchIds):
    url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account['accountId'] + '?beginIndex=' + str(i) + '&api_key=' + API
    temp = requests.get(url)
    while temp.status_code != 200:
        time.sleep(1)
        url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account['accountId'] + '?beginIndex=' + str(i) + '&api_key=' + API
        temp = requests.get(url)

    matches = temp.json()

    for match in matches['matches']:
        matchIds.append(match)

    return matchIds, matches['totalGames']


def getParticipantIdOfSummoner(participants, account):
    for participant in participants:
        if participant['player']['currentAccountId'] == account['accountId']: #maybe need to use if participant['player']['accountId'] instead
            return participant['participantId']


while True:
    print()
    summonerName = input('Summoner Name: ').lower()

    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + API
    summoner = requests.get(url)
    if summoner.status_code != 200:
        print(summoner.status_code)
        print('Summoner name not found, please try again')
        continue
    #403- api not valid
    #404- summoner name not found

    jprint(summoner.json())
    account = summoner.json() #Traits: accountId, id, name, summonerLevel

    #trying to get the rank
    url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + account['id'] + "?api_key=" + API
    temp = requests.get(url)
    if temp.status_code != 200:
        print('Summoner name not found, please try again')
        continue
    jprint(temp.json()) #returns an empty list if you are unranked. 

    #trying to get the match history
    matchIds = []
    i = 0
    
    matchIds, maxNumber = funfunsad(i, matchIds)
    i += 100

    while i < maxNumber:
        matchIds, maxNumber = funfunsad(i, matchIds)
        print(i)
        i += 100
    
    print("Number of matches played:" + str(len(matchIds))) #gets all of the matches from the last two years, though sometimes the helper function doesn't seem to work?

    latestMatch = matchIds[0]
    print('time of your last match....s upposedleyu :D')
    print(datetime.fromtimestamp(latestMatch['timestamp']//1000))



    print()
    print("Compiling the all matches from last two years into a json file.")

    before = time.time()
    i = 0
    while i < len(matchIds):
        match = matchIds[i]
        gameId = match['gameId']
        url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(match['gameId']) + "?api_key=" + API
        v4Match = requests.get(url)
        #url = 'https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/' + str(match['gameId']) + '?api_key=' +  API #timeline
        #v4Timeline = requests.get(url) #timeline
        if v4Match.status_code == 200: #and v4Timeline.status_code == 200: #could lead to infinite loop idk. #timeline
            #data for the Match
            v4Match = v4Match.json()
            participants = v4Match["participantIdentities"]
            participantIdOfSummoner = getParticipantIdOfSummoner(participants, account)
            participantStats = v4Match['participants']
            statsOfSummoner = None
            for participant in participantStats:
                if participant['participantId'] == participantIdOfSummoner:
                    statsOfSummoner = participant
            matchIds[i]['gameCreation'] = v4Match['gameCreation']//1000 #new addition
            matchIds[i]['gameDuration'] = v4Match['gameDuration'] #new addition
            matchIds[i]['summonerStats'] = statsOfSummoner
            matchIds[i]['everybodyStats'] = participantStats

            #data for the Timeline:
            #matchIds[i]['timeline'] = v4Timeline.json() #timeline. 
            i += 1
        elif v4Match.status_code == 429: #or v4Timeline.status_code == 429:
            #print('sleeping..' + str(i))
            estimatedTime = int((len(matchIds) - i) * 1.1)
            progress = int(100 - (len(matchIds)-i)/(len(matchIds))*100)
            print(f"Estimated Time remaining: {estimatedTime} seconds; progress: {progress}%")
            time.sleep(5)


    after = time.time()
    jprint(matchIds[0])
    print(after-before)
    print(len(matchIds))

    """
    time benchmarking if we do not use the timeline:
    for 111 matches: 34 seconds
    for 693 matches: 863 seconds

    time benchmarking if we do use the timeline as well:
    for 111 matches: 146 seconds
    for 693 matches: 1634 seconds
    """
    fileName = summonerName + 'Data.txt'
    with open(fileName, 'w') as outfile:
        json.dump(matchIds, outfile, indent=4)
    
    #with open(fileName) as json_file:
    #    testData = json.load(json_file)
    

    


