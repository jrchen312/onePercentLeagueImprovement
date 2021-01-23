#summoner gui.
#uses a modal app design,

from cmu_112_graphics import *
import json
import time

class MyModalApp(ModalApp):
    def appStarted(app):
        app.searchScreenMode = SearchScreen()
        app.summonerInfoMode = SummonerInfo()
        app.setActiveMode(app.searchScreenMode)
        app.timerDelay = 50

        #
        # API:
        app.api = "RGAPI-b961e6d3-0dbd-4161-b7c0-5f9a1a25acf9"
        #
        #
        app.summonerInfo = dict()

class SummonerInfo(Mode):
    def appStarted(self):
        SummonerInfo.loadRanks(self)
        SummonerInfo.loadChampionDetails(self)

        #drawing stuff
        self.pageLeft = 220
        #button:
        self.buttonSize = (32, 108)
        self.buttonLocation = (self.pageLeft+10, 200)

        SummonerInfo.summonerIconRank(self)
        SummonerInfo.preexistingMatchHistoryInformation(self)
        SummonerInfo.recentFifteenGames(self)

        self.updating = False
        self.matchIds = []
        self.currentMatchList = None
        self.i = 0
        self.j = 0
        self.progress = 0
        self.estimatedTime = 0


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


    def mousePressed(self, event):
        buttonX, buttonY = self.buttonLocation
        dy, dx = self.buttonSize
        buttonX1, buttonY1 = buttonX + dx, buttonY + dy
        if buttonX <= event.x <= buttonX1 and buttonY <= event.y <= buttonY1:
            print('UPDATING')
            self.updating = True

    def keyPressed(self, event):
        if event.x == "Enter":
            print(self.matchIds)


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
        else:
            self.estimatedTime = int((len(self.matchIds) - self.j) * 1.1)
            self.progress = int(100 - (len(self.matchIds)-self.j)/(len(self.matchIds))*100)
            print(f"Estimated Time remaining: {self.estimatedTime} seconds; progress: {self.progress}%")

    def getParticipantIdOfSummoner(self, participants):
        for participant in participants:
            if participant['player']['currentAccountId'] == self.app.summonerInfo['accountId']:
                return participant['participantId']


    def timerFired(self):
        if self.updating:
            SummonerInfo.updateController(self)


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
                print("FUCKIGN FINALLY POGGERS !!")
                SummonerInfo.appStarted(self)
        pass

    def redrawAll(self, canvas):
        #Header:
        pageLeft = self.pageLeft #120???
        #page color:
        canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, self.height, fill = "light blue", width = 0)

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
        #button:
        x, y = self.buttonLocation
        dy, dx = self.buttonSize
        x1, y1 = x +dx, y + dy
        color = 'light green' if self.updating else 'green'
        canvas.create_rectangle(x, y, x1, y1, fill=color, width = 0)
        canvas.create_text(x + (x1-x)/2, y + (y1-y)/2, fill='white', text="Update", font = "Arial 12 bold")

        #trying to draw the enemies:
        x0, y0, x1, y1 = pageLeft+370, 40, pageLeft+ 600, 235
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


app = MyModalApp(width=1280, height=720)