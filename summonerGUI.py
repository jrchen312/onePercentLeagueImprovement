#summoner gui.
#uses a modal app design,

from cmu_112_graphics import *
import json
import time


class Button(object):
    xsize = 64
    ysize = 30
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
    
    def draw(self, app, canvas):
        #canvas.create_rectangle(self.x-Button.xsize/2, self.y-Button.ysize/2, self.x + Button.xsize/2, self.y+Button.ysize/2)
        if app.sortingFactor == self.text:
            canvas.create_rectangle(self.x-Button.xsize/2, self.y-Button.ysize/2, self.x + Button.xsize/2, self.y+Button.ysize/2, fill='grey', width = 0)
        canvas.create_text(self.x, self.y, text=self.text)
    
    def pointInButton(self, px, py):
        if (self.x-Button.xsize/2 <= px <= self.x + Button.xsize/2 and
            self.y-Button.ysize/2 <= py <= self.y + Button.ysize/2):
            return self.text
        return None


class MyModalApp(ModalApp):
    def appStarted(app):
        app.searchScreenMode = SearchScreen()
        app.summonerInfoMode = SummonerInfo()
        app.setActiveMode(app.searchScreenMode)
        app.timerDelay = 50

        #
        # API:
        app.api = ""
        app.seasonStart = 1609920000 #time of start of season 11
        #
        #
        app.summonerInfo = dict()

class SummonerInfo(Mode):
    def appStarted(self):
        SummonerInfo.loadRanks(self)
        SummonerInfo.loadSummonerSpells(self)
        SummonerInfo.loadChampionDetails(self)
        SummonerInfo.loadQueueDetails(self)

        #drawing stuff
        self.pageLeft = 220
        #button:
        self.buttonSize = (32, 108)
        self.buttonLocation = (self.pageLeft+10, 200)

        SummonerInfo.summonerIconRank(self)
        SummonerInfo.preexistingMatchHistoryInformation(self)
        SummonerInfo.recentFifteenGames(self)

        self.updating = False
        self.preexisting = False
        self.matchIds = []
        self.currentMatchList = None
        self.i = 0
        self.j = 0
        self.progress = 0
        self.estimatedTime = 0

        self.mode = "overview" # "overview", "champions", "improvement"??
        self.modeButtonSize = (self.width-self.pageLeft*2)//3
        self.screenShift = 0
        self.scrolling = False
        self.initialScrollValue = 0

        self.gameStartIndex = 0
        self.numDisplayGames = 10
        minVal = len(self.matchHistory) if self.matchHistory != None else 0
        self.gameEndIndex = min(self.gameStartIndex + self.numDisplayGames, minVal)

        #loading information related to the champions--aggregate champion games and ranked stats: ('champions')
        self.sortingFactor = 'Games'
        self.descending = True
        SummonerInfo.loadAggregateStats(self)
        SummonerInfo.create_buttons(self)

    def loadAggregateStats(self):
        if self.matchHistory == None:
            self.aggregateGameStats = None
            self.rankedStats = None
            return
        self.aggregateGameStats = dict()
        self.rankedStats = {'games':0, 'wins':0, 'losses':0}
        for match in self.matchHistory:
            #match['timestamp'] is milliseconds epoch time, seasonStart is seconds
            if match['queue'] == 420 and match['timestamp']//1000 >= self.app.seasonStart: 
                self.rankedStats['games'] += 1
                if match['summonerStats']['stats']['win']:
                    self.rankedStats['wins'] += 1
                else:
                    self.rankedStats['losses'] += 1
            championPlayedKey = match['champion']
            championPlayed = self.IDtoChampion[str(championPlayedKey)]
            #champsPlayed[championPlayed] = champsPlayed.get(championPlayed, 0) + 1
            information = self.aggregateGameStats.get(championPlayed, None)

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
            information['totalMinionsKilled'] += match['summonerStats']['stats']['totalMinionsKilled'] + match['summonerStats']['stats']['neutralMinionsKilled']
            information['totalKills'] += match['summonerStats']['stats']['kills']
            information['totalDeaths'] += match['summonerStats']['stats']['deaths']
            information['totalAssists'] += match['summonerStats']['stats']['assists']
            information['gameDuration'] += match['gameDuration']


            self.aggregateGameStats[championPlayed] = information
        #print(self.aggregateGameStats) #dictionary form
        #print(SummonerInfo.sortDictionary(self, self.aggregateGameStats, 'gamesPlayed')) #list form. 

        self.championStats = dict()
        for key in self.aggregateGameStats:
            temp = dict()
            numGames = self.aggregateGameStats[key]['gamesPlayed']
            temp['Games'] = numGames
            temp['Wins'] = self.aggregateGameStats[key]['wins']
            temp['Losses'] = self.aggregateGameStats[key]['losses']
            temp['Win Rate'] = round(round(temp['Wins']/numGames, 3) * 100, 1)
            temp['Kills'] = round(self.aggregateGameStats[key]['totalKills']/numGames, 1)
            temp['Deaths'] = round(self.aggregateGameStats[key]['totalDeaths']/numGames, 1)
            temp['Assists'] = round(self.aggregateGameStats[key]['totalAssists']/numGames, 1)
            temp['Damage'] = round(self.aggregateGameStats[key]['totalDamage']/numGames, 1)
            temp['Dmg Taken'] = round(self.aggregateGameStats[key]['totalTaken']/numGames, 1)
            temp['Vision'] = round(self.aggregateGameStats[key]['visionScore']/numGames, 1)
            temp['Gold'] = round(self.aggregateGameStats[key]['goldEarned']/numGames, 1)
            temp['CS'] = round(self.aggregateGameStats[key]['totalMinionsKilled']/numGames, 1)
            temp['gameDuration'] = round(self.aggregateGameStats[key]['gameDuration']/numGames)
            self.championStats[key] = temp
        #print(self.championStats)

        self.sortedAggregateStats = SummonerInfo.sortDictionary(self, self.championStats, self.sortingFactor)
        self.sortedAggregateStats.reverse()
        #print(self.sortedAggregateStats)
        #buttons:
        #['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']



    def summonerIconRank(self):
        #loading in summoner Icon
        url = "https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon" + str(self.app.summonerInfo['profileIconId']) + ".png"
        self.summonerIcon = self.loadImage(url)
        self.summonerName = self.app.summonerInfo['name']
        self.summonerLevel = self.app.summonerInfo['summonerLevel']
        #Rank information
        if self.app.summonerInfo['tier'] == None:
            self.summonerRank = "Unranked"
            self.summonerTier = "unranked"
        else:
            self.summonerRank = self.app.summonerInfo['tier'].title() + " " +self.app.summonerInfo['rank']
            self.summonerTier = self.app.summonerInfo['tier'].lower()

    def preexistingMatchHistoryInformation(self):
        #Preexisting match history information
        file = self.summonerName.lower()
        for i in range(len(file)):
            if file[i] == " ":
                file = file[:i] + file[i+1:]
        fileName = file + 'Data.txt'
        try:
            with open(fileName) as json_file:
                self.matchHistory = json.load(json_file)
        except:
            self.matchHistory = None
            print("Existing match history not found!")

    def loadChampionDetails(self):
        versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
        latestVersion = versions.json()[0]
        championLinks = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion.json'
        championData = requests.get(championLinks)
        championToID = championData.json()['data']
        self.IDtoChampion = dict()
        for championName in championToID:
            self.IDtoChampion[championToID[championName]['key']] = championName
        self.championToID = championToID
        self.latestVersion = latestVersion

    def loadQueueDetails(self):
        gameModes = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
        #if gameModes.status_code == 200
        gameModes = gameModes.json()
        self.queueToDescription = dict()
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
            self.queueToDescription[dictionary['queueId']] = description
        #print(self.queueToDescription)

    #gets the kda, number of wins, number losses, total games?
    def recentFifteenGames(self):
        championsPlayed = dict()
        if self.matchHistory == None:
            print('Unable to obtain recentFifteenGames')
            self.fifteenStats = None
            return
        
        for i in range(20):
            try:
                match = self.matchHistory[i]
            except:
                print("skipp")
                continue #continue when there are less than 20/15 matches being played
            
            championPlayedKey = match['champion']
            championPlayed = self.IDtoChampion[str(championPlayedKey)]
            #championsPlayed[championPlayed] = championsPlayed.get(championPlayed, 0) + 1
            championInfo = championsPlayed.get(championPlayed, None)
            if championInfo == None:
                championInfo = dict()
                championInfo['games'] = 0
                championInfo['wins'] = 0
                championInfo['losses'] = 0
                championInfo['kills'] = 0
                championInfo['deaths'] = 0
                championInfo['assists'] = 0
            
            championInfo['kills'] += match['summonerStats']['stats']['kills']
            championInfo['deaths'] += match['summonerStats']['stats']['deaths']
            championInfo['assists'] += match['summonerStats']['stats']['assists']

            championInfo['games'] += 1
            if match['summonerStats']['stats']['win']:
                championInfo['wins'] += 1
            else:
                championInfo['losses'] += 1
            championsPlayed[championPlayed] = championInfo

        
        result = (self.sortDictionary(championsPlayed, 'games'))
        result.reverse()
        self.fifteenStats = result[:3]
        
        for dictionary in self.fifteenStats:
            for key in dictionary:
                tempKey = key
            url = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle.png'
            url2 = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle_0.png'
            url3 = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle_1.png'
            print(url2)
            print()
            try:
                tmep = self.loadImage(url)
                dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
                print(tmep.size)
            except:
                try:
                    tmep = self.loadImage(url2)
                    dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
                except:
                    tmep = self.loadImage(url3)
                    dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
        print(self.fifteenStats)


    def sortDictionary(self, dictionary, para):
        dictContents = []
        for key in dictionary:
            temp = dict()
            temp[key] = dictionary[key]
            dictContents.append(temp)
        #return dictContents

        n = len(dictContents)
        for startIndex in range(n):
            minIndex = startIndex
            for i in range(startIndex+1, n):
                tempDict = dictContents[i]
                for key in tempDict:
                    tempKey = key
                value1 = tempDict[tempKey][para]

                tempDict = dictContents[minIndex]
                for key in tempDict:
                    tempKey = key
                value2 = tempDict[tempKey][para]
                if (value1 <= value2):
                    minIndex = i
            SummonerInfo.swap(dictContents, startIndex, minIndex)
        return dictContents

    def swap(a, i, j):
        (a[i], a[j]) = (a[j], a[i])

    #this should be placed inside of a dictionary. 'unranked', 'bronze', .... 'challenger'
    def loadRanks(self):
        self.rankIcons = dict()
        temp = self.loadImage('images/Emblem_Iron.png')
        self.rankIcons['iron'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Bronze.png')
        self.rankIcons['bronze'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Silver.png')
        self.rankIcons['silver'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Gold.png')
        self.rankIcons['gold'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Platinum.png')
        self.rankIcons['platinum'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Diamond.png')
        self.rankIcons['diamond'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Master.png')
        self.rankIcons['master'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Grandmaster.png')
        self.rankIcons['grandmaster'] = self.scaleImage(temp, 1/6)
        temp = self.loadImage('images/Emblem_Challenger.png')
        self.rankIcons['challenger'] = self.scaleImage(temp, 1/6)

        self.rankIcons['unranked'] = self.rankIcons['challenger']

    #loads the summoner icons into self.summonerSpellIcons.
    #This could fail in the future, but removes need to use internet to slowly load these images in. 
    def loadSummonerSpells(self):
        self.summonerSpellIcons = dict()
        names = {'21': 'SummonerBarrier.png', '1': 'SummonerBoost.png', '14': 'SummonerDot.png', 
        '3': 'SummonerExhaust.png', '4': 'SummonerFlash.png', '6': 'SummonerHaste.png', 
        '7': 'SummonerHeal.png', '13': 'SummonerMana.png', '30': 'SummonerPoroRecall.png', 
        '31': 'SummonerPoroThrow.png', '11': 'SummonerSmite.png', '39': 'SummonerSnowURFSnowball_Mark.png', 
        '32': 'SummonerSnowball.png', '12': 'SummonerTeleport.png', '0': 'placeholder.png'} 

        for idNum in names:
            tempImg = self.loadImage('images/' + names[idNum])
            self.summonerSpellIcons[idNum] = self.scaleImage(tempImg, 1/2)
        #print(self.summonerSpellIcons)

    def mousePressed(self, event):
        buttonX, buttonY = self.buttonLocation
        dy, dx = self.buttonSize
        buttonX1, buttonY1 = buttonX + dx, buttonY + dy
        if buttonX <= event.x <= buttonX1 and buttonY <= event.y <= buttonY1:
            print('UPDATING')
            self.updating = True
            #getting the file name:
            file = self.summonerName.lower()
            for i in range(len(file)):
                if file[i] == " ":
                    file = file[:i] + file[i+1:]
            fileName = file + 'Data.txt'
            try:
                with open(fileName) as json_file:
                    self.preexisting = True
                    print('file found!')
            except:
                self.preexisting = False
                print('no file found!')
        ##################################
        #Code for the mode buttons: pretty poor practice
        #button1 position:
        buttonSize = self.modeButtonSize
        x0, y0, x1, y1 = self.pageLeft, 290, self.pageLeft+buttonSize, 320
        #button2 position:
        x2, y2, x3, y3 = self.pageLeft+ buttonSize, 290, self.pageLeft+buttonSize * 2, 320
        #button3 pos:
        x4, y4, x5, y5 = self.pageLeft + buttonSize*2, 290, self.pageLeft+buttonSize*3, 320
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            self.mode = "overview"
            self.screenShift = 0
        elif x2 <= event.x <= x3 and y2 <= event.y <= y3:
            self.mode = "champions"
            self.screenShift = 0
        elif x4 <= event.x <= x5 and y4 <= event.y <= y5:
            self.mode = "improvement"
            self.screenShift = 0
        
        ############
        # code for the buttons on the 'champions' screen
        if self.mode == 'champions':
            for button in self.buttons:
                result = button.pointInButton(event.x, event.y)
                if result != None and result != "Champion":
                    if result == self.sortingFactor:
                        self.descending = not self.descending
                    
                    self.sortingFactor = result
                    self.sortedAggregateStats = SummonerInfo.sortDictionary(self, self.championStats, self.sortingFactor)
                    if self.descending:
                        self.sortedAggregateStats.reverse()
                #buttons:
                #['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']
                # self.descending variable
        
        #################
        # scrolling?
        self.scrolling = True
        self.initialScrollValue = event.y
    
    def mouseDragged(self, event):
        self.screenShift += (self.initialScrollValue - event.y) * 2
        self.initialScrollValue = event.y

    def mouseReleased(self, event):
        self.scrolling = False #yeah, this is probably pretty useless lol
        print(self.screenShift, self.gameStartIndex)


    def keyPressed(self, event):
        if event.key == "Enter":
            pass

        elif event.key == "Down":
            self.screenShift += 25
        elif event.key == "Up":
            self.screenShift -= 25


    def matchIdLoader(self):
        url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.app.summonerInfo['accountId'] + '?beginIndex=' + str(self.i) + '&api_key=' + self.app.api
        temp = requests.get(url)
        if temp.status_code == 200:

            matches = temp.json()
            for match in matches['matches']:
                self.matchIds.append(match)
            
            self.currentMatchList = matches # ['totalGames']
            self.i += 100



    def matchJsonLoader(self):
        match = self.matchIds[self.j]
        gameId = match['gameId']
        url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(match['gameId']) + "?api_key=" + self.app.api
        v4Match = requests.get(url)
        if v4Match.status_code == 200:
            v4Match = v4Match.json()
            participants = v4Match["participantIdentities"]
            participantIdOfSummoner = SummonerInfo.getParticipantIdOfSummoner(self, participants)
            participantStats = v4Match['participants']
            statsOfSummoner = None
            for participant in participantStats:
                if participant['participantId'] == participantIdOfSummoner:
                    statsOfSummoner = participant
            self.matchIds[self.j]['gameCreation'] = v4Match['gameCreation']//1000 #new addition
            self.matchIds[self.j]['gameDuration'] = v4Match['gameDuration'] #new addition
            self.matchIds[self.j]['summonerStats'] = statsOfSummoner
            self.matchIds[self.j]['everybodyStats'] = participantStats
            self.j += 1
        
        self.estimatedTime = int((len(self.matchIds) - self.j) * 1.1)
        self.progress = int(100 - (len(self.matchIds)-self.j)/(len(self.matchIds))*100)
        #print(f"Estimated Time remaining: {self.estimatedTime} seconds; progress: {self.progress}%")

    def getParticipantIdOfSummoner(self, participants):
        for participant in participants:
            if participant['player']['currentAccountId'] == self.app.summonerInfo['accountId']:
                return participant['participantId']


    def timerFired(self):
        if self.updating and not self.preexisting:
            SummonerInfo.updateController(self)
        elif self.updating and self.preexisting:
            SummonerInfo.updatePreexistingController(self)
        
        if self.mode == 'overview':
            """
            self.gameStartIndex = 0
            self.numDisplayGames = 10
            minVal = len(self.matchHistory) if self.matchHistory != None else 0
            self.gameEndIndex = min(self.gameStartIndex + self.numDisplayGames, minVal)
            """
            start = 350
            size = 120
            buffer = 0
            
            temp = self.screenShift//(size + buffer)
            if temp < 0:
                temp = 0
            self.gameStartIndex = min(temp, len(self.matchHistory)-self.numDisplayGames)
            self.gameEndIndex = self.gameStartIndex + self.numDisplayGames

    def updatePreexistingController(self):
        #populating the self.matchIds list
        if self.currentMatchList == None:
            SummonerInfo.matchIdLoader(self)
            #time of the most recent match
            self.mostRecentMatchDate = self.matchHistory[0]['timestamp']
            #toggle variable.
            self.matchIdsPrepared = False
        elif self.i < self.currentMatchList['totalGames']:
            SummonerInfo.matchIdLoader(self)
        else:
            if not self.matchIdsPrepared:
                print(len(self.matchIds))
                self.matchIdsPrepared = True
                temp = []
                for match in self.matchIds:
                    if match['timestamp'] > self.mostRecentMatchDate:
                        temp.append(match)
                temp.reverse()
                self.matchIds = temp
                print(len(self.matchIds))
            elif self.j < len(self.matchIds):
                SummonerInfo.matchJsonLoader(self)
            else:
                self.updating = False
                #updating self.matchHistory
                for match in self.matchIds:
                    self.matchHistory.insert(0, match)
                #file Name:
                file = self.summonerName.lower()
                for i in range(len(file)):
                    if file[i] == " ":
                        file = file[:i] + file[i+1:]
                fileName = file + 'Data.txt'
                with open(fileName, 'w') as outfile:
                    json.dump(self.matchHistory, outfile, indent=4)
                SummonerInfo.appStarted(self)

    def updateController(self):
        if self.currentMatchList == None:
            SummonerInfo.matchIdLoader(self)
        elif self.i < self.currentMatchList['totalGames']:
            SummonerInfo.matchIdLoader(self)
        elif self.i >= self.currentMatchList['totalGames']:
            #need to start loading the match information, eventually storing it into a json file and restarting this app mode.
            #print(f"Number of matches: {len(self.matchIds)}")
            if self.j < len(self.matchIds):
                SummonerInfo.matchJsonLoader(self)
            else:
                self.updating = False
                file = self.summonerName.lower()
                for i in range(len(file)):
                    if file[i] == " ":
                        file = file[:i] + file[i+1:]
                fileName = file + 'Data.txt'
                with open(fileName, 'w') as outfile:
                    json.dump(self.matchIds, outfile, indent=4)
                SummonerInfo.appStarted(self)

    def redrawAll(self, canvas):
        #Header:
        pageLeft = self.pageLeft #120???
        #page color:
        canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, self.height, fill = "light blue", width = 0)

        #draw the mode:
        if self.mode == "overview":
            SummonerInfo.drawOverview(self, canvas)
        elif self.mode == "champions":
            SummonerInfo.drawChampions(self, canvas)
        elif self.mode == "improvement":
            SummonerInfo.drawImprovement(self, canvas)

        #draw a rectangle thing over the mode stuff to hide it :)
        canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, 340, fill = "light blue", width = 0)
        #icon image:
        canvas.create_image(pageLeft, 50, image=ImageTk.PhotoImage(self.summonerIcon), anchor = 'nw')
        #summonerlevel?
        canvas.create_rectangle(pageLeft + 32, 160, pageLeft + 96, 190, fill='black' )
        canvas.create_text(pageLeft + 64, 175, text=str(self.summonerLevel), fill="white", font="arial 11 bold")
        #summoner name text
        canvas.create_text(pageLeft + 150, 60, text=self.summonerName, anchor = 'nw', font='arial 28 bold')
        #rank
        canvas.create_image(pageLeft + 140, 110, image=ImageTk.PhotoImage(self.rankIcons[self.summonerTier]), anchor = 'nw')
        canvas.create_text(pageLeft + 240, 150, text=self.summonerRank, font = 'arial 14', anchor='w')
        #canvas.create_text(pageLeft + 240, 170, text=self.summonerRank, font = 'arial 14', anchor='w')
        #button:
        x, y = self.buttonLocation
        dy, dx = self.buttonSize
        x1, y1 = x +dx, y + dy
        color = 'light green' if self.updating else 'green'
        canvas.create_rectangle(x, y, x1, y1, fill=color, width = 0)
        canvas.create_text(x + (x1-x)/2, y + (y1-y)/2, fill='white', text="Update", font = "Arial 12 bold")

        #line position:
        x10, y10, x11, y11 = self.pageLeft, 320, self.width-self.pageLeft, 320
        #button1 position:
        buttonSize = self.modeButtonSize
        x0, y0, x1, y1 = self.pageLeft, 290, self.pageLeft+buttonSize, 320
        #button2 position:
        x2, y2, x3, y3 = self.pageLeft+ buttonSize, 290, self.pageLeft+buttonSize * 2, 320
        #button3 pos:
        x4, y4, x5, y5 = self.pageLeft + buttonSize*2, 290, self.pageLeft+buttonSize*3, 320
        #buttons with the different modes: # "overview", "champions", "improvement"??
        canvas.create_line(x10, y10, x11, y11)
        color = "grey" if self.mode == "overview" else None
        canvas.create_rectangle(x0, y0, x1, y1, fill = color)
        canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text="Overview")
        color = "grey" if self.mode == "champions" else None
        canvas.create_rectangle(x2, y2, x3, y3, fill = color)
        canvas.create_text(x2+(x3-x2)/2, y2+(y3-y2)/2, text="Champions")
        color = "grey" if self.mode == "improvement" else None
        canvas.create_rectangle(x4, y4, x5, y5, fill = color)
        canvas.create_text(x4+(x5-x4)/2, y4+(y5-y4)/2, text="Improvement")

        
        #if we are updating, draw the progress bar
        if self.updating:
            length = 400
            x0, y0, x1, y1 = pageLeft+100, 240, pageLeft+100 + length, 265
            canvas.create_rectangle(x0, y0, x1, y1)

            ext = self.progress/100* length
            canvas.create_rectangle(x0, y0, x0 + ext, y1, fill = 'green', width = 0)
            
            canvas.create_text(x0, y0 + 35, text=f"{self.estimatedTime} seconds remaining", anchor='w')


        #trying to draw the champions last played in 15 games:
        x0, y0, x1, y1 = pageLeft+600, 40, pageLeft+ 838, 235
        canvas.create_rectangle(x0, y0, x1, y1)
        if self.fifteenStats == None:
            canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text="No Stats Found", font = "arial 20", fill = "grey")
        else:

            for i in range(len(self.fifteenStats)):
                dictionary = self.fifteenStats[i]
                for key in dictionary:
                    pic = dictionary[key]['icon']
                    x2 = x0 + 36
                    y2 = y0 + 60 * i + 36
                    canvas.create_image(x2, y2, image=ImageTk.PhotoImage(pic))

                    #Draw champion name:
                    x3 = x2 + 36
                    y3 = y2 - 13
                    canvas.create_text(x3, y3, text=key, anchor = "w")

                    #Draw winrate and Wins/losses
                    x4 = x3
                    y4 = y3 + 24
                    wins = dictionary[key]['wins']
                    losses = dictionary[key]['losses']
                    winRate = int((wins / dictionary[key]['games']) * 100)
                    canvas.create_text(x4, y4, text=f"{winRate}%  ({wins}W {losses}L)", anchor = "w")

                    #Draw the KDA
                    x5 = x3 + 75
                    y5 = y4
                    killsAssists = dictionary[key]['kills'] + dictionary[key]['assists']
                    deaths = dictionary[key]['deaths']
                    kda = round(killsAssists/deaths, 2)
                    canvas.create_text(x5, y5, text=f"{kda} KDA", anchor = "w")


    def drawOverview(self, canvas):
        start = 350
        size = 120
        buffer = 15
        #canvas.create_rectangle(self.pageLeft, start, self.width-self.pageLeft, start + size)
        #canvas.create_text(self.width/2, start + size/2, text='work in progress')
        shift = self.screenShift
        startY = start - shift
        #trying to list out the first 10 matches
        for i in range(self.gameStartIndex, self.gameEndIndex):
            matchDetails = self.matchHistory[i]
            if matchDetails['summonerStats']['stats']['win']:
                color = SummonerInfo.rgbString(97, 194, 75) #random green
                victoryText = "Win"
            else:
                color = SummonerInfo.rgbString(226, 182, 179) #soft red
                victoryText  = "Loss"
            x0 = self.pageLeft
            y0 = startY + (size)*i+buffer
            x1 = self.width-self.pageLeft
            y1 = startY + (size) * (i+1)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            
            #queue !
            queue = self.queueToDescription[(matchDetails['queue'])]
            canvas.create_text(x0+40, y0 + size*(1/10), text=queue, font='calibri 10')

            min, sec = SummonerInfo.secondsToMinutes(matchDetails['gameDuration'])
            gameLength = f"{min}:{sec}"
            canvas.create_text(x0 + 40, y0 + size*(1/3), text=victoryText, font = 'calibri 14')
            canvas.create_text(x0 + 40, y0 + size*(2/3), text=gameLength, font = 'calibri 12')

            try:
                img1 = self.summonerSpellIcons[str(matchDetails['summonerStats']['spell1Id'])]
            except:
                img1 = self.summonerSpellIcons['0']
            try:
                img2 = self.summonerSpellIcons[str(matchDetails['summonerStats']['spell2Id'])]
            except:
                img2 = self.summonerSpellIcons['0']

            championPlayed = self.IDtoChampion[str(matchDetails['summonerStats']['championId'])]
            k = matchDetails['summonerStats']['stats']['kills']
            d = matchDetails['summonerStats']['stats']['deaths']
            a = matchDetails['summonerStats']['stats']['assists']

            kda = f"{k}/{d}/{a}"
            if d == 0:
                kd = f"KDA: {round(k+a, 2)}:1"
            else:
                kd = f"KDA: {round((k+a)/d, 2)}:1"
            canvas.create_text(x0 + 130, y0 + size*(2/5), text=championPlayed, font='calibri 18 bold')

            canvas.create_text(x0 + 300, y0 + size*(1/3), text=kda, font = 'calibri 12')
            canvas.create_text(x0 + 300, y0 + size*(2/3), text=kd, font = 'calibri 12')

            canvas.create_image(x0+220, y0 + size*(1/3)-5, image=ImageTk.PhotoImage(img1))
            canvas.create_image(x0+220, y0 + size*(2/3)-5, image=ImageTk.PhotoImage(img2))

            date = time.strftime('%m-%d-%Y', time.localtime(matchDetails['timestamp']//1000))
            t = time.strftime('%H:%M', time.localtime(matchDetails['timestamp']//1000))
            #date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(matchDetails['timestamp'])) #[:10]
            canvas.create_text(x1 - 100, y0 + size*(1/3), text=date, font='calibri 12')
            canvas.create_text(x1 - 100, y0 + size*(2/3), text=t, font='calibri 12')
    
    def secondsToMinutes(seconds):
        sec = seconds % 60
        min = seconds // 60
        return min, sec


    
    def drawChampions(self, canvas):
        if self.aggregateGameStats == None:
            return
        start = 350+Button.ysize/2
        canvas.create_line(self.pageLeft, start, self.width-self.pageLeft, start)
        for button in self.buttons:
            button.draw(self, canvas)
        
        shift = self.screenShift
        y = start + Button.ysize - shift
        x = Button.xsize/2 + self.pageLeft
        k = 0 #k is the amount of vertical distance
        for dictionary in self.sortedAggregateStats:
            for key in dictionary:

                #does not display the champion if the number of games is less than 5. 
                if dictionary[key]['Games'] < 5:
                    k-=1
                    continue #?
                
                yTextPos = y+Button.ysize*(1+k)
                if yTextPos < start + Button.ysize/2:
                    continue
                canvas.create_text(x, yTextPos, text=key)
                championStats = dictionary[key]
                i = 0 #i is the horizontal distance. 
                for key in championStats:
                    if key == 'gameDuration': continue
                    canvas.create_text(x+Button.xsize*(1+i), y+Button.ysize*(1+k), text=championStats[key])
                    i += 1
            k += 1 


    def create_buttons(self):
        #creating the buttons
        self.buttons = []
        x = Button.xsize/2 + self.pageLeft
        y = 350
        self.buttons.append(Button(x, y, 'Champion'))
        traits = ['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']
        for i in range(len(traits)):
            self.buttons.append(Button(x+Button.xsize*(1+i),y, traits[i]))

    def drawImprovement(self, canvas):
        start = 350
        size = 120
        canvas.create_rectangle(self.pageLeft, start, self.width-self.pageLeft, start + size)
        canvas.create_text(self.width/2, start + size/2, text='work in progress')

    #code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

class SearchScreen(Mode):
    def appStarted(self):
        self.typeCursor = True
        self.typeCursorFrame = 0
        self.typeCursorFrames = 4

        self.summonerName = ""
        self.error = None
        
        self.summonerInformation = None


    def keyPressed(self, event):
        if len(event.key) == 1:
            self.summonerName += event.key
        elif event.key == 'Space':
            self.summonerName += " "
        elif event.key == "Backspace":
            length = len(self.summonerName)
            self.summonerName = self.summonerName[0:length-1]
        elif event.key == "Enter":
            if len(self.summonerName) > 0:
                if SearchScreen.summonerNameValid(self):
                    self.app.summonerInfo = self.summonerInformation
                    self.summonerName = ""
                    print(self.app.summonerInfo)
                    self.app.setActiveMode(self.app.summonerInfoMode)

    def summonerNameValid(self):
        url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.summonerName + "?api_key=" + self.app.api
        summoner = requests.get(url)
        self.error = None
        if summoner.status_code == 403:
            print("API invalid")
            self.error = 403
            return False
        elif summoner.status_code == 404:
            print("Summoner name not found")
            self.error = 404
            return False
        elif summoner.status_code != 200:
            print("unknown error")
            return False
        self.summonerInformation = summoner.json()
        
        #rank information:
        url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self.summonerInformation['id'] + "?api_key=" + self.app.api
        temp = requests.get(url)
        if temp.status_code == 200:
            if temp.json() != []:
                self.summonerInformation['tier'] = temp.json()[0]['tier']  # Bronze
                self.summonerInformation['rank'] = temp.json()[0]['rank']  # I
            else:
                self.summonerInformation['tier'] = None
                self.summonerInformation['rank'] = None
        else:
            self.summonerInformation['tier'] = None
            self.summonerInformation['rank'] = None
        return True

    def timerFired(self):
        SearchScreen.typingCursorSetting(self)

    def typingCursorSetting(self):
        self.typeCursorFrame = (self.typeCursorFrame + 1) % self.typeCursorFrames
        if self.typeCursorFrame == 0:
            self.typeCursor = not self.typeCursor

    def redrawAll(self, canvas):
        SearchScreen.drawSearchScreen(self, canvas)

    #code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


    def drawSearchScreen(self, canvas):
        backgroundColor = SearchScreen.rgbString(158, 189, 233)
        canvas.create_rectangle(0, 0, self.width, self.height, fill= backgroundColor)
        canvas.create_text(self.width//2, self.height//4, text="SummonerGUI", font = "arial 36 bold")

        #dimensions of the search box:
        w = self.width//3
        h = 80
        canvas.create_rectangle(self.width//2-w, self.height//2 - h, self.width//2+w, self.height//2, fill = "white", width = 0)
        champText = self.summonerName + "|" if self.typeCursor else self.summonerName

        if champText == "|" or champText == "":
            canvas.create_text(self.width//2 - w + 20, self.height//2-h + 25, text = "Enter Summoner Name.", anchor = 'nw', font = "helvetica 20", fill = "grey")

        canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, text=champText, font = "helvetica 24", anchor = 'nw')
        SearchScreen.drawError(self, canvas, w, h)

    def drawError(self, canvas, w, h):
        if self.error != None:
            if self.error == 403:
                canvas.create_text(self.width//2-w, self.height//2-h-17, text="Invalid API.", fill = "red", anchor = "w", font = "helvetica 12")
            elif self.error == 404:
                canvas.create_text(self.width//2-w, self.height//2-h-17, text="Summoner name not found", fill = "red", anchor = "w", font = "helvetica 12")
            else:
                canvas.create_text(self.width//2-w, self.height//2-h-17, text="Error, try again", fill = "red", anchor = "w", font = "helvetica 12")


app = MyModalApp(width=1280, height=1000)