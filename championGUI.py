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
    self.championScreenIndex = 0

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
                self.championScreenIndex = 0
                #obtainChampionStats(self)
    else:
        if event.key == 'Escape':
            self.searchScreen = True
            self.championName = ""
        elif event.key == "Space":
            self.championScreenIndex = 0
        elif event.key == "q":
            self.championScreenIndex = 1
        elif event.key == "w":
            self.championScreenIndex = 2
        elif event.key == "e":
            self.championScreenIndex = 3
        elif event.key == "r":
            self.championScreenIndex = 4
        elif event.key == "Enter":
            self.hideText = not self.hideText
        print(self.championScreenIndex)

def mousePressed(self, event):
    if not self.searchScreen:
        if 1 <= self.championScreenIndex <= 5:
            if pointInChampIcon(self, event.x, event.y):
                self.championScreenIndex = 0
        elif self.championScreenIndex == 0:
            result = pointInWhichIcon(self, event.x, event.y)
            if result != None:
                self.championScreenIndex = result

        
def pointInChampIcon(self, px, py):
    y = self.height/2 + 20
    x = self.width/4
    xSize, ySize = self.championIcon.size
    lowerX = x - xSize/2
    upperX = x + xSize/2
    lowerY = y - ySize/2
    upperY = y + ySize/2
    if lowerX <= px <= upperX and lowerY <= py <= upperY:
        return True
    return False

def pointInWhichIcon(self, px, py):
    height = self.height *3/4 + 40
    spacing = 75
    
    images = [(self.width/2 - spacing, height), (self.width/2, height), (self.width/2 + spacing, height), 
              (self.width/2 + spacing * 2, height), (self.width/2 + spacing * 3, height)]
    for i in range(len(images)):
        (x, y) = images[i]
        if pointInAbilityIcon(self, x, y, px, py):
            if i == 0:
                return 5 #5 will be passive
            else:
                return i
    return None

def pointInAbilityIcon(self, imgX, imgY, px, py):
    imgSize = 32
    lowerX = imgX - imgSize
    upperX = imgX + imgSize
    lowerY = imgY - imgSize
    upperY = imgY + imgSize
    if lowerX <= px <= upperX and lowerY <= py <= upperY:
        return True
    return False
def obtainChampionStats(self):
    print('LOADING.........')
    #creates an API link based on the lastestVersion global variable and the championName that the user inputted. 
    championLink = 'http://ddragon.leagueoflegends.com/cdn/' + self.latestVersion + '/data/en_US/champion/' + self.championName + '.json'

    championData = requests.get(championLink)
    self.championData = championData
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
        self.championTip = "N/A"
    

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
    loadAbilityData(self)
    loadIcons(self)
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
    
def loadIcons(self):
    url = 'https://ddragon.leagueoflegends.com/cdn/' + self.latestVersion + '/img/champion/' + self.championName + '.png' 
    self.championIcon = self.loadImage(url)

    #self.passiveIcon
    passiveName = self.passive['image']['full']
    url = 'https://ddragon.leagueoflegends.com/cdn/' + self.latestVersion + '/img/passive/' + passiveName
    self.passiveIcon = self.loadImage(url)

    spellName = self.q['image']['full']
    url = "https://ddragon.leagueoflegends.com/cdn/" + self.latestVersion + "/img/spell/" + spellName
    self.qIcon = self.loadImage(url)

    spellName = self.w['image']['full']
    url = "https://ddragon.leagueoflegends.com/cdn/" + self.latestVersion + "/img/spell/" + spellName
    self.wIcon = self.loadImage(url)

    spellName = self.e['image']['full']
    url = "https://ddragon.leagueoflegends.com/cdn/" + self.latestVersion + "/img/spell/" + spellName
    self.eIcon = self.loadImage(url)

    spellName = self.r['image']['full']
    url = "https://ddragon.leagueoflegends.com/cdn/" + self.latestVersion + "/img/spell/" + spellName
    self.rIcon = self.loadImage(url)


def loadAbilityData(self):
    self.q = self.championData.json()['data'][self.championName]['spells'][0]
    self.w = self.championData.json()['data'][self.championName]['spells'][1]
    self.e = self.championData.json()['data'][self.championName]['spells'][2]
    self.r = self.championData.json()['data'][self.championName]['spells'][3]
    self.passive = self.championData.json()['data'][self.championName]['passive']

    


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

    if not self.hideText:
        if self.championScreenIndex == 0:
            championHomeScreen(self, canvas)
        elif self.championScreenIndex == 1:
            #drawQInfo(self, canvas)
            ability, name, description, cost, costType, cooldown, damage, icon = getInformation(self, 1)
            drawAbilityPage(self, canvas, ability, name, description, cost, costType, cooldown, damage, icon)
        elif self.championScreenIndex == 2:
            ability, name, description, cost, costType, cooldown, damage, icon = getInformation(self, 2)
            drawAbilityPage(self, canvas, ability, name, description, cost, costType, cooldown, damage, icon)
        elif self.championScreenIndex == 3:
            ability, name, description, cost, costType, cooldown, damage, icon = getInformation(self, 3)
            drawAbilityPage(self, canvas, ability, name, description, cost, costType, cooldown, damage, icon)
        elif self.championScreenIndex == 4:
            ability, name, description, cost, costType, cooldown, damage, icon = getInformation(self, 4)
            drawAbilityPage(self, canvas, ability, name, description, cost, costType, cooldown, damage, icon)
        elif self.championScreenIndex == 5:
            ability, name, description, icon = getPassiveInformation(self)
            drawAbilityPassivePage(self, canvas, ability, name, description, icon)


def championHomeScreen(self, canvas):
    w = 400
    h = 400

    drawTextBackground(self, canvas)

    championTitle = self.championName.upper() + ", " +self.championTitle
    canvas.create_text(self.width//2, self.height//2, fill = "white", text = championTitle, font = "arial 30 bold")

    championAttribute = f"{self.championName} is a {self.championAttributes}."
    canvas.create_text(self.width//2, self.height//2 + 50, fill = "white", text = championAttribute, font = "arial 20 bold")

    tip = "A tip: " + self.championTip
    if len(tip) > 70:
        i = len(tip) // 2
        tip = tip[:i] + '-\n' + tip[i:]
    canvas.create_text(self.width//2, self.height//2 + 100, fill = "white", text = tip, font = "arial 12")

    difficulty = "Champion Difficulty: " + str(self.championDifficulty) + "/10"
    canvas.create_text(self.width//2, self.height//2 + 150, fill = "white", text = difficulty)

    height = self.height *3/4 + 40
    spacing = 75
    canvas.create_image(self.width/3, height, image=ImageTk.PhotoImage(self.championIcon))
    canvas.create_image(self.width/2 - spacing, height, image=ImageTk.PhotoImage(self.passiveIcon))
    canvas.create_image(self.width/2, height, image=ImageTk.PhotoImage(self.qIcon))
    canvas.create_image(self.width/2 + spacing, height, image=ImageTk.PhotoImage(self.wIcon))
    canvas.create_image(self.width/2 + spacing * 2, height, image=ImageTk.PhotoImage(self.eIcon))
    canvas.create_image(self.width/2 + spacing * 3, height, image=ImageTk.PhotoImage(self.rIcon))
    
    textHeight = height + 45
    #canvas.create_text(self.width/3, textHeight+25, text="Stats", fill = "white", font = "arial 12 bold") #down a little because the icon is larger. 
    canvas.create_text(self.width/2 - spacing, textHeight, text="Passive", fill = "white", font = "arial 12 bold")
    canvas.create_text(self.width/2, textHeight, text="Q", fill = "white", font = "arial 12 bold")
    canvas.create_text(self.width/2 + spacing, textHeight, text="W", fill = "white", font = "arial 12 bold")
    canvas.create_text(self.width/2 + spacing*2, textHeight, text="E", fill = "white", font = "arial 12 bold")
    canvas.create_text(self.width/2 + spacing*3, textHeight, text="R", fill = "white", font = "arial 12 bold")
    




def drawQInfo(self, canvas):
    drawTextBackground(self, canvas)
    height = self.height * 3/4
    canvas.create_image(self.width/3, height, image=ImageTk.PhotoImage(self.qIcon))

    description = self.q['description']
    canvas.create_text(self.width//2, self.height//2 + 40, text= description)
    
def drawTextBackground(self, canvas):
    w = 400
    h = 400
    lovelyblack = rgbString(30, 34, 52)
    canvas.create_rectangle(self.width/2-w, self.height/2-50, self.width/2+w, self.height/2+h, fill = lovelyblack)
    

def drawAbilityPage(self, canvas, ability, name, description, cost, costType, cooldown, damage, icon):
    drawTextBackground(self, canvas)
    championTitle = self.championName.upper()
    canvas.create_text(self.width//2, self.height//2, fill = "white", text = championTitle, font = "arial 30 bold")

    height = self.height/2 + 20
    canvas.create_image(self.width/4, height, image=ImageTk.PhotoImage(self.championIcon))

    iconX = self.width/4
    iconY = height + 100
    canvas.create_image(iconX, iconY, image=ImageTk.PhotoImage(icon))
    canvas.create_text(iconX, iconY + 44, text=ability, font = 'arial 14 bold', fill = 'white')

    textMarginX = iconX + 50
    canvas.create_text(textMarginX, iconY - 20, text=name, font = 'arial 14 bold', fill = 'white', anchor = 'w')
    canvas.create_text(textMarginX, iconY, text=description, font = 'arial 10', fill = 'white', anchor = 'nw')

    textMarginY = iconY + 75
    canvas.create_text(textMarginX, textMarginY, text=f"Cooldown: {cooldown}", font = 'arial 10', fill = 'white', anchor = 'w')
    canvas.create_text(textMarginX, textMarginY+20, text=f"Cost: {cost}, resource: {costType}", font = 'arial 10', fill = 'white', anchor = 'w')

    canvas.create_text(textMarginX, textMarginY+40, text=f"Damage: {damage}", font = 'arial 10', fill = 'white', anchor = 'w')


def drawAbilityPassivePage(self, canvas, ability, name, description, icon):
    drawTextBackground(self, canvas)
    championTitle = self.championName.upper()
    canvas.create_text(self.width//2, self.height//2, fill = "white", text = championTitle, font = "arial 30 bold")

    height = self.height/2 + 20
    canvas.create_image(self.width/4, height, image=ImageTk.PhotoImage(self.championIcon))

    iconX = self.width/4
    iconY = height + 100
    canvas.create_image(iconX, iconY, image=ImageTk.PhotoImage(icon))
    canvas.create_text(iconX, iconY + 44, text=ability, font = 'arial 14 bold', fill = 'white')

    textMarginX = iconX + 50
    canvas.create_text(textMarginX, iconY - 20, text=name, font = 'arial 14 bold', fill = 'white', anchor = 'w')
    canvas.create_text(textMarginX, iconY, text=description, font = 'arial 10', fill = 'white', anchor = 'nw')


def getPassiveInformation(self):
    ability = "Passive"
    description = self.passive['description']
    name = self.passive['name']
    icon = self.passiveIcon

    return ability, name, description, icon

    
def getInformation(self, index):
    if index == 1: # Q
        ability = 'Q'
        description = self.q['description']
        name = self.q['name']
        cost = self.q['cost']
        costType = self.q['costType']
        cooldown = self.q['cooldown']
        damage = self.q['effect'][1]
        icon = self.qIcon
    elif index == 2: # W
        ability = 'W'
        description = self.w['description']
        name = self.w['name']
        cost = self.w['cost']
        costType = self.w['costType']
        cooldown = self.w['cooldown'] 
        damage = self.w['effect'][1]
        icon = self.wIcon
    elif index == 3: # E
        ability = 'E'
        description = self.e['description']
        name = self.e['name']
        cost = self.e['cost']
        costType = self.e['costType']
        cooldown = self.e['cooldown']
        damage = self.e['effect'][1]
        icon = self.eIcon
    else:
        ability = 'R'
        description = self.r['description']
        name = self.r['name']
        cost = self.r['cost']
        costType = self.r['costType']
        cooldown = self.r['cooldown']
        damage = self.r['effect'][1]
        icon = self.rIcon
    
    # a whole lot of things to decrease the issues...
    while description.find('<br><br>') != -1:
        i = description.find('<br><br>')
        description = description[:i] + ' ' + description[i+8:]
    delimiter = False
    i = 0
    while i < len(description):
        if description[i] == "<":
            delimiter = True
        if delimiter:
            if description[i] == ">":
                delimiter = False
            description = description[:i] + description[i+1:]
        else:
            i += 1

    while description.find('. ') != -1:
        i = description.find('. ')
        description = description[:i] + '.\n' + description[i+2:]

    if costType == " {{ abilityresourcename }}":
        costType = "Mana"
    
    return ability, name, description, cost, costType, cooldown, damage, icon


"""
    self.q['cooldown'] # list of cooldown
    self.q['cost'] #how much mana
    self.q['costType'] #needs to be processed
    self.q['description'] # description string
    self.q['effect'][1] #amount of damage?? need more processing i assume
    self.q['image']['full'] #icon image from league api
"""
def searchScreen(self, canvas):
    backgroundColor = rgbString(205, 170, 200)
    canvas.create_rectangle(0, 0, self.width, self.height, fill= backgroundColor)
    canvas.create_text(self.width//2, self.height//4, text="ChampionGUI", font = "arial 36 bold")

    #dimensions of the search box:
    w = self.width//3
    h = 80
    canvas.create_rectangle(self.width//2-w, self.height//2 - h, self.width//2+w, self.height//2, fill = "white", width = 0)
    champText = self.championName + "|" if self.typeCursor else self.championName

    if champText == "|" or champText == "":
        canvas.create_text(self.width//2 - w + 20, self.height//2-h + 25, text = "Enter Champion Name.", anchor = 'nw', font = "helvetica 20", fill = "grey")

    canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, text=champText, font = "helvetica 24", anchor = 'nw')

    if self.failedAttempt:
        canvas.create_text(self.width//2-w, self.height//2-h-17, text="Name not found in database. Try again.", fill = "red", anchor = "w", font = "helvetica 12")

    if self.loading:
        canvas.create_text(self.width//2-w, self.height//2-h-17, text="Loading...", fill = "Black", anchor = "w", font = "helvetica 12")

#################################################
# main
#################################################

runApp(width = 1280, height = 720)