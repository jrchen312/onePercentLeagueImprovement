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

def keyPressed(self, event):

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



def isValidName(self):
    championName = self.championName.title().strip()
    # ISSUE: doesn't work for lee sin.
    i = championName.find(" ")
    while i != -1:
        championName = championName[0:i] + championName[i+1:] 
        i = championName.find(" ")

    if championName not in self.championDicts:
        return False
    return True


def timerFired(self):
    typingCursorSetting(self)

def typingCursorSetting(self):
    self.typeCursorFrame = (self.typeCursorFrame + 1) % self.typeCursorFrames
    if self.typeCursorFrame == 0:
        self.typeCursor = not self.typeCursor

#code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def redrawAll(self, canvas):
    searchScreen(self, canvas)

def searchScreen(self, canvas):
    backgroundColor = rgbString(205, 170, 200)
    canvas.create_rectangle(0, 0, self.width, self.height, fill= backgroundColor)
    canvas.create_text(self.width//2, self.height//4, text="ChampionGUI by Jeff Chen", font = "arial 36 bold")

    #dimensions of the search box:
    w = self.width//3
    h = 80
    canvas.create_rectangle(self.width//2-w, self.height//2 - h, self.width//2+w, self.height//2, fill = "white", width = 0)
    champText = self.championName + "|" if self.typeCursor else self.championName
    canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, text=champText, font = "helvetica 24", anchor = 'nw')

    if self.failedAttempt:
        canvas.create_text(self.width//2-w, self.height//2-h-17, text="Name not found in database. Try again.", fill = "red", anchor = "w", font = "helvetica 12")

#################################################
# main
#################################################

runApp(width = 1280, height = 720)