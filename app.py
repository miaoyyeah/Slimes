from cmu_graphics import *
from PIL import Image
import math

from slimesManager import SlimesManager
from baseMap import BaseMap
import baseMap
from button import Button
import generateMap

def onAppStart(app):
    app.width = 900
    app.height = 630
    app.r = 100
    app.stepsPerSecond = 1

    evaluateIndex = [i for i in range(6)]
    app.evaluateMap = loadMap(evaluateIndex, app.width/2 - app.r, 
                              app.height/2 - 2.5*app.r,
                              2.5*app.r, 0.8*app.r, 3, 2)
    
    app.helpMapList = loadHelpMap(app)
    app.helpSlimeManager = loadHelp(app)

    app.welcome_buttonList = welcome_loadButton(app)
    app.evaluate_buttonList = evaluate_loadButton(app)
    app.game_buttonList = game_loadButton(app)
    app.level_buttonList = level_loadButton(app)
    app.help_buttonList = help_loadButton(app)

    app.curScreen = 'welcome'
    app.prevScreen = []
    
    app.remindTime = 2
    app.isPause = False

    loadBackGround(app)
    loadWheel(app)
    loadHelpBg(app)
    loadSlimeManager(app, generateMap.generateMap(7))

def loadSlimeManager(app, mapList):
    app.status = 'new'
    app.gameMap = loadMap(mapList, app.width/2, app.height/2, 
                1.12*app.r, 3**0.5*1.12*app.r/2)
    app.tmpMapList = mapList
    app.slimesManager = SlimesManager(app.gameMap)
    app.evaluateSlimeList = SlimesManager.loadSlimeList(app.evaluateMap)
    app.counter = app.gameMap.counter
    app.counterRectWidth = 450
    app.counterFill = 'papayaWhip'
    app.hintStatus = False
    app.grading = None

def loadBackGround(app):
    app.bgImg = Image.open(f"images/background.png")
    app.bgImg = app.bgImg.resize((app.width, app.height))
    app.bgImg = CMUImage(app.bgImg)

def loadMap(indexList, x, y, d, h, rows = 0, cols = 0):
    if isinstance(indexList, str):
        indexList = baseMap.getIndexList(indexList)
    return BaseMap(indexList, x, y, d, h, rows, cols)

def loadHelp(app):
    helpSlimeList = []
    for helpMap in app.helpMapList:
        newManager = SlimesManager(helpMap)
        helpSlimeList.append(newManager)
    return helpSlimeList

def loadWheel(app):
    app.wheelImg = Image.open(f"images/slimeWheel.png")
    app.wheelImg = app.wheelImg.resize((150, 150))
    app.wheelImg = CMUImage(app.wheelImg)

def loadHelpMap(app):
    helpIndexList = [[0, 2], [2, 4], [0, 0]]
    mapList = []
    x, y = app.width/2 - 0.5*app.r, app.height/2 - 2.5*app.r
    for helpIndex in helpIndexList:
        y += 1.5*app.r
        mapList.append(loadMap(helpIndex, x, y, app.r, app.r, 1, 2))
    return mapList

def drawBackGround(app):
    drawImage(app.bgImg, 0, 0)

def drawButton(buttonList):
    for button in buttonList:
        button.draw()

def onButtonPress(app, screenName, mouseX, mouseY):
    buttonList = getattr(app, f"{screenName}_buttonList")
    for button in buttonList:
        if button.checkForPress(mouseX, mouseY):
            button.onMousePressButton(mouseX, mouseY)

def onButtonRelease(app, screenName, mouseX, mouseY):
    buttonList = getattr(app, f"{screenName}_buttonList")
    for button in buttonList:
        if button.checkForPress(mouseX, mouseY):
            buttonFun = button.onMouseReleaseButton(mouseX, mouseY)
            if buttonFun != None:
                screenManage(app, buttonFun)

def backButtonFunction(app):
    if app.curScreen == 'help':
        app.helpSlimeManager = loadHelp(app)
    setActiveScreen(app.prevScreen[-1])
    app.curScreen = app.prevScreen.pop()
    if app.curScreen == 'welcome' and app.status != 'new':
        loadSlimeManager(app, generateMap.generateMap(7))

def screenManage(app, screenName):
    setActiveScreen(screenName)
    if screenName == 'welcome':
        app.curScreen = 'welcome'
        app.prevScreen = []
    elif app.curScreen == 'help':
        app.curScreen = app.prevScreen.pop()
    else:
        app.prevScreen.append(app.curScreen)
        app.curScreen = screenName

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
    drawBackGround(app)
    drawLabel("SLIMES", app.width/2, app.height/2 - 50, size = 50)
    drawButton(app.welcome_buttonList)

def welcome_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'welcome', mouseX, mouseY)
    if app.status != 'new':
        loadSlimeManager(app, generateMap.generateMap(7))

def welcome_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'welcome', mouseX, mouseY)

def welcome_onStep(app):
    pass

#---level_buttons---------------------------------------------------------------

def simpleButtonFunction(app):
    loadSlimeManager(app, generateMap.generateMap(7))
    screenManage(app, 'game')

def standardButtonFunction(app):
    loadSlimeManager(app, generateMap.generateMap(10))
    screenManage(app, 'game')

def hardButtonFunction(app):
    loadSlimeManager(app, generateMap.generateMap(13))
    screenManage(app, 'game')

#---level-----------------------------------------------------------------------

def level_loadButton(app):
    simpleButton = Button(simpleButtonFunction, text = 'Simple level')
    standardButton = Button(standardButtonFunction, text = 'Standard level')
    hardButton = Button(hardButtonFunction, text = 'Hard level')
    buttonList = [simpleButton, standardButton, hardButton]
    y = -(len(buttonList) - 1) * 80/2
    for button in buttonList:
        button.x = app.width/2
        button.y = app.height/2 + 150 + y
        y += 80
    backButton = Button(backButtonFunction, text = 'Back', width = 100, 
                        x = 770, y = app.height - 50, selectFun = False)
    buttonList.append(backButton)
    return buttonList

def level_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'level', mouseX, mouseY)

def level_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'level', mouseX, mouseY)

def level_redrawAll(app):
    drawBackGround(app)
    drawLabel("SELECT LEVEL", app.width/2, app.height/2 - 50, size = 30)
    drawButton(app.level_buttonList)

#---help Button-----------------------------------------------------------------

def resetButtonFunction(app):
    app.helpSlimeManager = loadHelp(app)

#---help------------------------------------------------------------------------
def loadHelpBg(app):
    app.helpImg = Image.open(f"images/help.png")
    app.helpImg = app.helpImg.resize((app.width, app.height))
    app.helpImg = CMUImage(app.helpImg)

def help_loadButton(app):
    resetButton = Button(resetButtonFunction, text = 'Reset', width = 100, 
                         x = 770, y = app.height - 130)
    backButton = Button(backButtonFunction, text = 'Back', width = 100, 
                        x = 770, y = app.height - 50, selectFun = False)
    buttonList = [resetButton, backButton]
    return buttonList

def help_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'help', mouseX, mouseY)
    for manager in app.helpSlimeManager:
        manager.mousePressSlimes(mouseX, mouseY)

def help_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'help', mouseX, mouseY)

def help_redrawAll(app):
    drawImage(app.helpImg, 0, 0)
    drawImage(app.wheelImg, app.width/2 + 3 * app.r, app.height/2 - 2 * app.r, 
            align = 'center')
    for manager in app.helpSlimeManager:
        manager.drawSlimes()
        manager.drawPair()
    drawButton(app.help_buttonList)
    
#---game_buttons----------------------------------------------------------------

def resetButton(app):
    app.game_buttonList[1].fill = 'lightGray'
    app.game_buttonList[2].fill = 'lightGray'

def hintButtonFunction(app):
    if app.slimesManager.hint != None and not app.isPause:
        app.hintStatus = not app.hintStatus

def undoButtonFunction(app):
    if app.slimesManager.undoMix != None and not app.isPause:
        app.slimesManager.undo()
        app.game_buttonList[1].fill = 'lightGray'
        app.game_buttonList[2].fill = 'papayaWhip'

def redoButtonFunction(app):
    if app.slimesManager.redoMix != None and not app.isPause:
        app.slimesManager.redo()
        app.game_buttonList[2].fill = 'lightGray'
        app.game_buttonList[1].fill = 'papayaWhip'

def reStartButtonFunction(app):
    loadSlimeManager(app, app.tmpMapList)
    if app.curScreen != 'game':
        app.curScreen = app.prevScreen.pop()
        setActiveScreen(app.curScreen)

def pauseButtonFunction(app):
    app.isPause = not app.isPause
    if app.isPause:
        app.game_buttonList[4].text = 'Continue'
    else:
        app.game_buttonList[4].text = 'Pause'

#---game------------------------------------------------------------------------
def drawTimeCounter(app):
    drawLabel(app.counter, 100, 40, size=30)
    drawRect(150, 40, app.counterRectWidth, 20, 
             fill = app.counterFill, align = 'left')
    drawRect(150, 40, 450, 20, fill = None, 
             border = 'black', align = 'left')

def game_loadButton(app):
    hintButton = Button(hintButtonFunction, 'Hint')
    undoButton = Button(undoButtonFunction, 'Undo', fill = 'lightGray')
    redoButton = Button(redoButtonFunction, 'Redo', fill = 'lightGray')
    reStartButton = Button(reStartButtonFunction, 'Restart')
    pauseButton = Button(pauseButtonFunction, 'Pause', selectFun = False)
    helpButton = Button('help', 'Help')
    backButton = Button(backButtonFunction, 'Back', selectFun = False)
    buttonList = [hintButton, undoButton, redoButton, 
                  reStartButton, pauseButton, helpButton, backButton]
    x = 0
    for button in buttonList:
        button.x = 100 + x
        button.y = app.height - 50
        button.width = 90
        x += 120
    return buttonList

def game_onMousePress(app, mouseX, mouseY):
    if not app.isPause:
        app.status = app.slimesManager.mousePressSlimes(mouseX, mouseY)
        if app.status == 'win' or app.status == 'lose':
            loadGrading(app)
            screenManage(app, 'evaluate')
        if app.slimesManager.undoMix != None:
            app.game_buttonList[1].fill = 'papayaWhip'
        if app.slimesManager.redoMix == None:
            app.game_buttonList[2].fill = 'lightGray'
    onButtonPress(app, 'game', mouseX, mouseY)

def game_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'game', mouseX, mouseY)

def game_onStep(app):
    if not app.isPause:
        if app.counter > 0:
            app.counter -= 1
            app.counterRectWidth -= 400 / app.gameMap.counter
        if app.counter < 10:
            app.counterFill = 'tomato'
        if app.counter == 0:
            app.status = 'lose'
            loadGrading(app)
            screenManage(app, 'evaluate')
        if not app.slimesManager.mixLegal:
            app.remindTime -= 1
            if app.remindTime == 0:
                app.slimesManager.mixLegal = True
                app.remindTime = 2

def game_redrawAll(app):
    drawBackGround(app)
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
    if not app.slimesManager.mixLegal:
        app.slimesManager.drawRemind()

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

def loadGrading(app):
    grading = math.floor(app.counter * 5 / app.gameMap.counter)
    gradingList = ['D', 'C', 'B', 'A', 'S']
    app.gradeImage = Image.open(f"images/grading/{gradingList[grading]}.png")
    app.gradeImage = app.gradeImage.resize((3*app.r, 3*app.r))
    app.gradeImage = CMUImage(app.gradeImage)

def drawGrading(app):
    if app.gradeImage != None:
        drawImage(app.gradeImage, 150, 150, align = 'center')

def evaluate_loadButton(app):
    backButton = Button('welcome', 'Back', app.width/2, 
                        app.height/2 + 2.5*app.r, selectFun = False)
    reStartButton = Button(reStartButtonFunction, 'Restart', app.width/2, 
                           app.height/2 + 3*app.r)
    buttonList = [backButton, reStartButton]
    return buttonList

def evaluate_redrawAll(app):
    drawBackGround(app)
    timeBonus = app.counter*10
    levelScore = app.gameMap.level*100
    totalScore = timeBonus + levelScore + app.slimesManager.score
    drawLabel(f"You {app.status} the game!", 
              app.width/2, app.height/2 - 20, size = 20)
    drawLabel(f"Time left: {app.gameMap.counter}", 
              app.width/2, app.height/2 + 20, size = 20)
    drawLabel(f"Time bonus: {timeBonus}", 
            app.width/2, app.height/2 + 60, size = 20)
    drawLabel(f"Level score: {levelScore}", 
        app.width/2, app.height/2 + 100, size = 20)
    drawLabel(f"Remove score: {app.slimesManager.score}", 
              app.width/2, app.height/2 + 140, size = 20)
    drawLabel(f"Total score: {totalScore}", 
            app.width/2, app.height/2 + 180, size = 20)
    drawGrading(app)
    drawSlimeCount(app)
    drawButton(app.evaluate_buttonList)

def evaluate_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'evaluate', mouseX, mouseY)

def evaluate_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'evaluate', mouseX, mouseY)

def main():
    runApp()

runAppWithScreens(initialScreen='welcome')