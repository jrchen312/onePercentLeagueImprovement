import json
import requests
import math


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

#champion to id
championToID = championData.json()['data']
IDtoChampion = dict()

for championName in championToID:
    IDtoChampion[championToID[championName]['key']] = championName



while True:
    print()
    summonerName = input("Enter summoner name: ").lower().strip()
    fileName = summonerName + 'Data.txt'
    try:
        with open(fileName) as json_file:
            testData = json.load(json_file)
    except:
        print("did not work, you have to load the summoner data in")
        testData = None
        #exit the program. 
        continue

    #ranked stats. creates a list of 
    aggregateChampionStats = dict()
    rankedMatches = []
    rankedStats = {'games':0, 'wins':0, 'losses':0}
    for match in testData:
        if match['queue'] == 420:
            rankedMatches.append(match)
            rankedStats['games'] += 1
            if match['summonerStats']['stats']['win']:
                rankedStats['wins'] += 1
            else:
                rankedStats['losses'] += 1
        championPlayedKey = match['champion']
        championPlayed = IDtoChampion[str(championPlayedKey)]
        #champsPlayed[championPlayed] = champsPlayed.get(championPlayed, 0) + 1
        information = aggregateChampionStats.get(championPlayed, None)

        #not necessarily effective, but it's "neater"
        if information == None: 
            information = dict()
            information['gamesPlayed'] = 0
            information['wins'] = 0
            information['losses'] = 0
            #stats
            information['totalDamage'] = 0
            information['totalTaken'] = 0
            information['visionScore'] = 0
            information['goldEarned'] = 0
            information['totalMinionsKilled'] = 0
            #KDA
            information['totalKills'] = 0
            information['totalDeaths'] = 0
            information['totalAssists'] = 0
            #game
            information['gameDuration'] = 0
            information['rankedMatches'] = 0
        
        if match['queue'] == 420:
            information['rankedMatches'] += 1
        if match['summonerStats']['stats']['win']:
            information['wins'] += 1
        else:
            information['losses'] += 1
        information['gamesPlayed'] += 1

        information['totalDamage'] += match['summonerStats']['stats']['totalDamageDealtToChampions']
        information['totalTaken'] += match['summonerStats']['stats']['totalDamageTaken']
        information['visionScore'] += match['summonerStats']['stats']['visionScore']
        information['goldEarned'] += match['summonerStats']['stats']['goldEarned']
        information['totalMinionsKilled'] += match['summonerStats']['stats']['totalMinionsKilled']
        information['totalKills'] += match['summonerStats']['stats']['kills']
        information['totalDeaths'] += match['summonerStats']['stats']['deaths']
        information['totalAssists'] += match['summonerStats']['stats']['assists']
        information['gameDuration'] += match['gameDuration']


        aggregateChampionStats[championPlayed] = information

        #to get aggregate stats (number of games won, lost, total games, damage done, damage taken, vision score, gold, KDA!, cS per minute, 
    print("Number of ranked matches: " + str(len(rankedMatches)))
    print("Champions Played: " + str(aggregateChampionStats))
    print(rankedStats)


    #Trying to get the aggregate stats of this now:
    while True:
        champName = input("Enter a champion name: ")
        try:
            champId = championToID[champName]['key']
        except:
            print('did not work')
            continue
        print(champId)
        champId = int(champId)

        specificChampionGames = []
        specificChampionVictories = []
        specificChampionDefeats = []
        for game in rankedMatches:
            #print(game['champion'], champId, type(game['champion']), type(champId))
            if game['champion'] == champId:
                specificChampionGames.append(game)
                if game['summonerStats']['stats']['win']:
                    specificChampionVictories.append(game)
                else:
                    specificChampionDefeats.append(game)
        print(len(specificChampionGames))
        print(len(specificChampionVictories), len(specificChampionDefeats))

        specificChampionVictories.reverse()
        specificChampionVictoriesFives = []
        sampleSize = 10
        upper = math.ceil(len(specificChampionVictories)/sampleSize)
        for i in range(0, upper):
            lower = i*sampleSize
            upper = min((i+1)*sampleSize, len(specificChampionVictories))
            fiveGameAggregate = dict()
            fiveGameAggregate['totalDamage'] = 0
            fiveGameAggregate['totalTaken'] = 0
            fiveGameAggregate['visionScore'] = 0
            fiveGameAggregate['goldEarned'] = 0
            fiveGameAggregate['totalMinionsKilled'] = 0
            #KDA
            fiveGameAggregate['totalKills'] = 0
            fiveGameAggregate['totalDeaths'] = 0
            fiveGameAggregate['totalAssists'] = 0
            #game
            fiveGameAggregate['gameDuration'] = 0
            fiveGameAggregate['visionWardsBoughtInGame'] = 0
            fiveGameAggregate['sampleSize'] = 0
            for k in range(lower, upper):
                match = specificChampionVictories[k]
                fiveGameAggregate['totalDamage'] += match['summonerStats']['stats']['totalDamageDealtToChampions']
                fiveGameAggregate['totalTaken'] += match['summonerStats']['stats']['totalDamageTaken']
                fiveGameAggregate['visionScore'] += match['summonerStats']['stats']['visionScore']
                fiveGameAggregate['goldEarned'] += match['summonerStats']['stats']['goldEarned']
                fiveGameAggregate['totalMinionsKilled'] += match['summonerStats']['stats']['totalMinionsKilled']
                fiveGameAggregate['totalKills'] += match['summonerStats']['stats']['kills']
                fiveGameAggregate['totalDeaths'] += match['summonerStats']['stats']['deaths']
                fiveGameAggregate['totalAssists'] += match['summonerStats']['stats']['assists']
                fiveGameAggregate['visionWardsBoughtInGame'] += match['summonerStats']['stats']['visionWardsBoughtInGame']
                fiveGameAggregate['gameDuration'] += match['gameDuration']
                fiveGameAggregate['sampleSize'] += 1
            specificChampionVictoriesFives.append(fiveGameAggregate)

        jprint(specificChampionVictoriesFives)

        temp = specificChampionVictoriesFives[0]
        for key in temp:
            trait = []
            for dictionary in specificChampionVictoriesFives:
                numMinutes = dictionary['gameDuration']//60 #number of minutes
                trait.append(dictionary[key]/numMinutes)
            print(key, trait)
        
        print(specificChampionVictories[0]['gameCreation']) #game creation per minute
        print(specificChampionVictories[-1]['gameCreation'])
        break




    



