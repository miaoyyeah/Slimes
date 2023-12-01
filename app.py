from cmu_graphics import *
from slimesManager import SlimesManager
from baseMap import BaseMap
import baseMap
from button import Button
import generateMap
from PIL import Image

def onAppStart(app):
    app.width = 858
    app.height = 600
    app.r = 100
    evaluateIndex = [i for i in range(6)]
    app.evaluateMap = loadMap(evaluateIndex, 'rectGrid', 
                              app.width/2 - app.r, app.height/2 - 2.5*app.r,
                              2.5*app.r, 0.8*app.r, 3, 2)
    app.stepsPerSecond = 1
    app.welcome_buttonList = welcome_loadButton(app)
    app.evaluate_buttonList = evaluate_loadButton(app)
    app.game_buttonList = game_loadButton(app)
    loadSlimeManager(app)
    loadWheel(app)

def loadSlimeManager(app):
    app.gameMap = loadMap(generateMap.generateMap(7), 'hexGrid', 
                          app.width/2, app.height/2, 
                          1.2*app.r, 3**0.5*1.2*app.r/2)
    app.slimesManager = SlimesManager(app.gameMap)
    app.evaluateSlimeList = SlimesManager.loadSlimeList(app.evaluateMap)
    app.counter = app.gameMap.counter
    app.counterRectWidth = 500
    app.counterFill = 'papayaWhip'
    app.status = 'new'
    app.hintStatus = False

def loadMap(indexList, gridType, x, y, d, h, rows = 0, cols = 0):
    if isinstance(indexList, str):
        indexList = baseMap.getIndexList(indexList)
    return BaseMap(indexList, gridType, x, y, d, h, rows, cols)

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
        buttonFun = button.onMouseReleaseButton(mouseX, mouseY)
        if buttonFun != None:
            setActiveScreen(buttonFun)

#---welcome---------------------------------------------------------------------

def welcome_loadButton(app):
    startButton = Button('game', text = 'Start')
    missionButton = Button('level', text = 'Level')
    helpButton = Button('help', text = 'Help')
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

#---game_buttons----------------------------------------------------------------

def hintButtonFunction(app):
    if app.slimesManager.hint != None:
        app.hintStatus = not app.hintStatus

def undoButtonFunction(app):
    if app.slimesManager.undoMix != None:
        app.slimesManager.undo()

def redoButtonFunction(app):
    if app.slimesManager.redoMix != None:
        app.slimesManager.redo()

#---game------------------------------------------------------------------------
def drawTimeCounter(app):
    drawLabel(app.counter, 100, 100, size=30)
    drawRect(150, 100, app.counterRectWidth, 20, 
             fill = app.counterFill, align = 'left')
    drawRect(150, 100, 500, 20, fill = None, 
             border = 'black', align = 'left')

def game_loadButton(app):
    hintButton = Button(hintButtonFunction, 'Hint')
    undoButton = Button(undoButtonFunction, 'Undo')
    redoButton = Button(redoButtonFunction, 'Redo')
    buttonList = [hintButton, undoButton, redoButton]
    y = 0
    for button in buttonList:
        button.x = 100
        button.y = 300 + y
        button.width = 100
        y += 80
    return buttonList

def game_onMousePress(app, mouseX, mouseY):
    app.status = app.slimesManager.mousePressSlimes(mouseX, mouseY)
    if app.status == 'win' or app.status == 'lose':
        setActiveScreen('evaluate')
    onButtonPress(app, 'game', mouseX, mouseY)

def game_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'game', mouseX, mouseY)

def game_onStep(app):
    if app.counter > 0:
        app.counter -= 1
        app.counterRectWidth -= 400 / app.gameMap.counter
    if app.counter < 10:
        app.counterFill = 'tomato'
    if app.counter == 0:
        app.status = 'lose'
        setActiveScreen('evaluate')

def game_redrawAll(app):
    app.slimesManager.drawSlimes()
    drawTimeCounter(app)
    drawButton(app.game_buttonList)
    drawImage(app.wheelImg, app.width/2 + 3 * app.r, app.height/2 - 2 * app.r, 
              align = 'center')
    drawLabel(f"Your Point: {app.slimesManager.score}", 
              app.width/2 + 3 * app.r, app.height/2 - app.r, size = 20)
    app.slimesManager.drawPair()
    if app.hintStatus:
        app.slimesManager.drawHint()

#---evaluate--------------------------------------------------------------------
def loadSlimeCount(app):
    countList = []
    for slime in app.evaluateSlimeList:
        countList.append(f"X {app.slimesManager.slimeCount[slime.index]}")
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
    backButton = Button('welcome', 'Back', app.width/2, app.height/2 + 2*app.r)
    buttonList = [backButton]
    return buttonList

def evaluate_redrawAll(app):
    timeBonus = app.counter*10
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