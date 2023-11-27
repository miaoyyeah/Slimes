from cmu_graphics import *
from baseSlimes import BaseSlimes
from slimesManager import SlimesManager
from baseMap import BaseMap
import baseMap
from button import Button
from PIL import Image

def onAppStart(app):
    app.width = 858
    app.height = 600
    app.r = 100
    app.evaluateMap = loadMap(BaseSlimes.getSlimeName(), 'rectGrid', 
                              app.width/2 - app.r, app.height/2 - 2.5*app.r,
                              2.5*app.r, 0.8*app.r, 3, 2)
    app.stepsPerSecond = 1
    app.welcome_buttonList = welcome_loadButton(app)
    app.evaluate_buttonList = evaluate_loadButton(app)
    loadSlimeManager(app)
    loadWheel(app)

def loadSlimeManager(app):
    app.gameMap = loadMap('baseMap1', 'hexGrid', app.width/2, app.height/2, 
                      1.2*app.r, 3**0.5*1.2*app.r/2)
    app.slimesManager = SlimesManager(app.gameMap)
    app.evaluateSlimeList = SlimesManager.loadSlimeList(app.evaluateMap)
    app.status = 'new'

def loadMap(nameList, gridType, x, y, d, h, rows = 0, cols = 0):
    if isinstance(nameList, str):
        nameList = baseMap.getNameList(nameList)
    return BaseMap(nameList, gridType, x, y, d, h, rows, cols)

def loadWheel(app):
    app.wheelImg = Image.open(f"images/slimeWheel.png")
    app.wheelImg = app.wheelImg.resize((150, 150))
    app.wheelImg = CMUImage(app.wheelImg)

def drawButton(buttonList):
    for button in buttonList:
        button.draw()

def onButtonPress(app, screenName, mouseX, mouseY):
    buttonList = globals()[f"{screenName}_loadButton"](app)
    for button in buttonList:
        button.onMousePressButton(mouseX, mouseY)

def onButtonRelease(app, screenName, mouseX, mouseY):
    buttonList = globals()[f"{screenName}_loadButton"](app)
    for button in buttonList:
        buttonName = button.onMouseReleaseButton(mouseX, mouseY)
        if buttonName != None:
            setActiveScreen(buttonName)

#---welcome---------------------------------------------------------------------
def welcome_loadButton(app):
    startButton = Button('Start', 'game')
    missionButton = Button('Mission', 'mission')
    helpButton = Button('Help', 'help')
    buttonList = [startButton, missionButton, helpButton]
    y = -(len(buttonList) - 1) * 80/2
    for button in buttonList:
        button.x = app.width/2
        button.y = app.height/2 + 150 + y
        y += 80
    return buttonList

def welcome_redrawAll(app):
    drawLabel("SLIMES", app.width/2, app.height/2 - 50, size = 50)
    drawButton(app.welcome_buttonList)

def welcome_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'welcome', mouseX, mouseY)
    if app.status != 'new':
        loadSlimeManager(app)

def welcome_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'welcome', mouseX, mouseY)

def welcome_onStep(app):
    if app.status != 'new':
        loadSlimeManager(app)

#---game------------------------------------------------------------------------

def game_onMousePress(app, mouseX, mouseY):
    app.status = app.slimesManager.mousePressSlimes(mouseX, mouseY)
    if app.status == 'win':
        setActiveScreen('evaluate')

def game_onStep(app):
    if app.gameMap.counter > 0:
        app.gameMap.counter -= 1
    elif app.gameMap.counter == 0:
        app.status = 'lose'
        setActiveScreen('evaluate')

def game_redrawAll(app):
    app.slimesManager.drawSlimes()
    drawLabel(app.gameMap.counter, 200, 200, size=50)
    drawImage(app.wheelImg, app.width/2 + 3 * app.r, app.height/2 - 2 * app.r, 
              align = 'center')

#---evaluate--------------------------------------------------------------------
def loadSlimeCount(app):
    countList = []
    for slime in app.evaluateSlimeList:
        countList.append(f"X {app.slimesManager.slimeCount[slime.name]}")
    return countList

def drawSlimeCount(app):
    countList = loadSlimeCount(app)
    posList = BaseMap.rectGrid(app.width/2, app.height/2 - 2.5*app.r, 
                               2.5*app.r, 0.8*app.r, 3, 2)
    for i in range(6):
        app.evaluateSlimeList[i].draw()
        x, y = posList[i]
        drawLabel(countList[i], x, y, size = 20)

def evaluate_loadButton(app):
    backButton = Button('back', 'welcome', app.width/2, app.height/2 + 2*app.r)
    buttonList = [backButton]
    return buttonList

def evaluate_redrawAll(app):
    timeBonus = app.gameMap.counter*10
    levelScore = app.gameMap.level*100
    totalScore = timeBonus + levelScore + app.slimesManager.score
    drawLabel(f"You {app.status} the game!", 
              app.width/2, app.height/2 - 60, size = 20)
    drawLabel(f"Time left: {app.gameMap.counter}", 
              app.width/2, app.height/2 - 20, size = 20)
    drawLabel(f"Time bonus: {timeBonus}", 
            app.width/2, app.height/2 + 20, size = 20)
    drawLabel(f"Level score: {levelScore}", 
        app.width/2, app.height/2 + 60, size = 20)
    drawLabel(f"Remove score: {app.slimesManager.score}", 
              app.width/2, app.height/2 + 100, size = 20)
    drawLabel(f"Total score: {totalScore}", 
            app.width/2, app.height/2 + 140, size = 20)
    drawSlimeCount(app)
    drawButton(app.evaluate_buttonList)

def evaluate_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'evaluate', mouseX, mouseY)

def evaluate_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'evaluate', mouseX, mouseY)

def main():
    runApp()

runAppWithScreens(initialScreen='welcome')