#import championStats
from cmu_112_graphics import *
import requests
import json
import random

def appStarted(self):
    #pre data processing:
    versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
    self.latestVersion = versions.json()[0]

    #link: http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json
    championLinks = 'http://ddragon.leagueoflegends.com/cdn/' + self.latestVersion + '/data/en_US/champion.json'

    championData = requests.get(championLinks)
    #print(championData.json())

    self.championDicts = championData.json()['data']

    self.championName = ""
    self.failedAttempt = False
    self.typeCursor = True
    self.typeCursorFrame = 0
    self.typeCursorFrames = 4

    self.searchScreen = True
    self.hideText = False

    self.loading = False

def keyPressed(self, event):
    if self.searchScreen:
        if len(event.key) == 1:
            self.championName += event.key
        elif event.key == 'Space':
            self.championName += " "
        elif event.key == "Backspace":
            length = len(self.championName)
            self.championName = self.championName[0:length-1]
        elif event.key == "Enter":
            if not isValidName(self):
                self.failedAttempt = True
            else:
                self.failedAttempt = False
                self.searchScreen = False
                self.loading = True
                #obtainChampionStats(self)
    else:
        if event.key == 'Escape':
            self.searchScreen = True
        else:
            self.hideText = not self.hideText


def obtainChampionStats(self):
    print('LOADING.........')
    #creates an API link based on the lastestVersion global variable and the championName that the user inputted. 
    championLink = 'http://ddragon.leagueoflegends.com/cdn/' + self.latestVersion + '/data/en_US/champion/' + self.championName + '.json'

    championData = requests.get(championLink)
    if (championData.status_code) != 200:
        print("Something is wrong, please try again.")
        print(self.championName)

    championName = championData.json()['data'][self.championName]['id']
    self.championTitle = championData.json()['data'][championName]['title'].title()

    championSkinDict = championData.json()['data'][championName]['skins']
    self.championSkinNums = []
    for dictionary in championSkinDict:
        self.championSkinNums.append(dictionary['num'])
    
    self.championLore = championData.json()['data'][championName]['lore']

    try:
        self.championTip = random.choice(championData.json()['data'][championName]['allytips'])
    except:
        self.championTip = "Nvm, don't have one XD"
    

    championAttributesList = championData.json()['data'][championName]['tags']
    self.championAttributes = championAttributesList[0]
    for i in range(1, len(championAttributesList)):
        self.championAttributes = self.championAttributes + "/" + championAttributesList[i]
    #print(f"{championName} is a {championAttributes}")
    
    self.championDifficulty = championData.json()['data'][championName]['info']['difficulty']
    #print("Champion Difficulty: " + str(championDifficulty) + "/10")

    championStats = championData.json()['data'][championName]['stats']
    #print(championStats)

    self.baseHP = championStats['hp']
    self.hpperlevel = championStats['hpperlevel']

    self.baseMP = championStats['mp']
    self.mpperlevel = championStats['mpperlevel']

    self.armor = championStats['armor']
    self.amorperlevel = championStats['armorperlevel']

    self.magicresist = championStats['spellblock']
    self.magicresisterperlevel = championStats['spellblockperlevel']

    self.hpregen = championStats['hpregen']
    self.hpregenperlevel = championStats['hpregenperlevel']

    self.mpregen = championStats['mpregen']
    self.mpregenperlevel = championStats['mpregenperlevel']

    self.crit = championStats['crit']
    self.critperlevel = championStats['critperlevel']

    self.attackdamage = championStats['attackdamage']
    self.attackdamageperlevel = championStats['attackdamageperlevel']

    self.attackspeed = championStats['attackspeed']
    self.attackspeedperlevel = championStats['attackspeedperlevel']

    self.movespeed = championStats['movespeed']
    self.attackrange = championStats['attackrange']

    loadSkins(self)
    self.loading = False


def loadSkins(self):
    skinIDs = (self.championSkinNums[1:])
    random.shuffle(skinIDs)
    skinIDs = (skinIDs[:1])
    print(skinIDs)
    self.championSkins = []
    for id in skinIDs:
        #url format: https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sona_7.jpg
        url = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + self.championName + "_" + str(id) + ".jpg"
        
        self.championSkins.append(self.loadImage(url))
    #random.shuffle(self.championSkins)
    

def isValidName(self):
    championName = self.championName.title().strip()
    # ISSUE: doesn't work for lee sin. (works now, jk)
    i = championName.find(" ")
    while i != -1:
        championName = championName[0:i] + championName[i+1:] 
        i = championName.find(" ")

    if championName not in self.championDicts:
        return False
    self.championName = championName
    return True


def timerFired(self):
    if self.searchScreen:
        typingCursorSetting(self)
    if self.loading:
        obtainChampionStats(self)

def typingCursorSetting(self):
    self.typeCursorFrame = (self.typeCursorFrame + 1) % self.typeCursorFrames
    if self.typeCursorFrame == 0:
        self.typeCursor = not self.typeCursor

#code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def redrawAll(self, canvas):
    if self.searchScreen or self.loading:
        searchScreen(self, canvas)
    else:
        championScreen(self, canvas)


def championScreen(self, canvas):
    background = self.championSkins[0]
    canvas.create_image(self.width//2, self.height//2, image=ImageTk.PhotoImage(background))

    w = 300
    h = 400

    if not self.hideText:
        lovelyblack = rgbString(30, 34, 52)
        canvas.create_rectangle(self.width/2-w, self.height/2-50, self.width/2+w, self.height/2+h, fill = lovelyblack)

        championTitle = self.championName.upper() + ", " +self.championTitle
        canvas.create_text(self.width//2, self.height//2, fill = "white", text = championTitle, font = "arial 30 bold")

        championAttribute = f"{self.championName} is a {self.championAttributes}"
        canvas.create_text(self.width//2, self.height//2 + 50, fill = "white", text = championAttribute, font = "arial 20 bold")

        tip = "A tip: " + self.championTip
        if len(tip) > 70:
            i = len(tip) // 2
            tip = tip[:i] + '-\n' + tip[i:]
        canvas.create_text(self.width//2, self.height//2 + 100, fill = "white", text = tip, font = "arial 12")

        difficulty = "Champion Difficulty: " + str(self.championDifficulty) + "/10"
        canvas.create_text(self.width//2, self.height//2 + 150, fill = "white" ,text = difficulty)


def searchScreen(self, canvas):
    backgroundColor = rgbString(205, 170, 200)
    canvas.create_rectangle(0, 0, self.width, self.height, fill= backgroundColor)
    canvas.create_text(self.width//2, self.height//4, text="ChampionGUI", font = "arial 36 bold")

    #dimensions of the search box:
    w = self.width//3
    h = 80
    canvas.create_rectangle(self.width//2-w, self.height//2 - h, self.width//2+w, self.height//2, fill = "white", width = 0)
    champText = self.championName + "|" if self.typeCursor else self.championName
    canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, text=champText, font = "helvetica 24", anchor = 'nw')

    if self.failedAttempt:
        canvas.create_text(self.width//2-w, self.height//2-h-17, text="Name not found in database. Try again.", fill = "red", anchor = "w", font = "helvetica 12")

    if self.loading:
        canvas.create_text(self.width//2-w, self.height//2-h-17, text="Loading...", fill = "Black", anchor = "w", font = "helvetica 12")

#################################################
# main
#################################################

runApp(width = 1280, height = 720)