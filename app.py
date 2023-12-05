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
    app.stepsPerSecond = 4

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
    resetButton(app)
    app.status = 'new'
    app.gameMap = loadMap(mapList, app.width/2, app.height/2, 
                1.12*app.r, 3**0.5*1.12*app.r/2)
    app.tmpMapList = mapList
    app.slimesManager = SlimesManager(app.gameMap)
    app.evaluateSlimeList = SlimesManager.loadSlimeList(app.evaluateMap)
    app.stepCount = 0
    app.counter = app.gameMap.counter
    app.counterRectWidth = 450
    app.counterFill = 'papayaWhip'
    app.hintStatus = False
    app.grading = None

def loadBackGround(app):
    app.bgImg = Image.open(f"images/background.png")
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
    app.wheelImg = CMUImage(app.wheelImg)

def loadHelpMap(app):
    helpIndexList = [[0, 2], [2, 4], [0, 0]]
    mapList = []
    x, y = app.width/2 - 0.5*app.r, app.height/2 - 2.5*app.r
    for helpIndex in helpIndexList:
        y += 1.5*app.r
        mapList.append(loadMap(helpIndex, x, y, app.r, app.r, 1, 2))
    return mapList

def drawBackGround(app, bgImg = 'default'):
    if bgImg == 'default':
        drawImage(app.bgImg, 0, 0)
    else:
        drawImage(bgImg, 0, 0)

def drawButton(buttonList):
    for button in buttonList:
        button.draw()

def onButtonPress(app, screenName, mouseX, mouseY):
    buttonList = getattr(app, f"{screenName}_buttonList")
    for button in buttonList:
        if button.checkForPress(mouseX, mouseY):
            button.onMousePressButton()

def onButtonRelease(app, screenName, mouseX, mouseY):
    buttonList = getattr(app, f"{screenName}_buttonList")
    for button in buttonList:
        if button.checkForPress(mouseX, mouseY):
            if not ((button.text == 'Undo' and 
                     app.slimesManager.undoMix == None) or 
                    (button.text == 'Redo' and 
                     app.slimesManager.redoMix == None)):
                buttonFun = button.onMouseReleaseButton()
                if buttonFun != None:
                    screenManage(app, buttonFun)

def onButtonMove(app, screenName, mouseX, mouseY):
    buttonList = getattr(app, f"{screenName}_buttonList")
    for button in buttonList:
        button.onMouseMoveButton(mouseX, mouseY)

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
    startButton = Button('game', text = 'Start', width = 150)
    missionButton = Button('level', text = 'Level', width = 150)
    helpButton = Button('help', text = 'Help', width = 150)
    buttonList = [startButton, missionButton, helpButton]
    y = -(len(buttonList) - 1) * 80/2
    for button in buttonList:
        button.x = app.width/2
        button.y = app.height/2 + 150 + y
        y += 80
    return buttonList

def welcome_redrawAll(app):
    img = Image.open(f"images/welcome_background.png")
    img = CMUImage(img)
    drawBackGround(app, img)
    drawButton(app.welcome_buttonList)

def welcome_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'welcome', mouseX, mouseY)
    if app.status != 'new':
        loadSlimeManager(app, generateMap.generateMap(7))

def welcome_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'welcome', mouseX, mouseY)

def welcome_onMouseMove(app, mouseX, mouseY):
    onButtonMove(app, 'welcome', mouseX, mouseY)

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
    simpleButton = Button(simpleButtonFunction, text = 'Simple', 
                          width = 150, selectFun = False)
    standardButton = Button(standardButtonFunction, selectFun = False, 
                            text = 'Standard', width = 150)
    hardButton = Button(hardButtonFunction, selectFun = False, 
                        text = 'Hard', width = 150)
    buttonList = [simpleButton, standardButton, hardButton]
    y = -(len(buttonList) - 1) * 80/2
    for button in buttonList:
        button.x = app.width/2
        button.y = app.height/2 + 150 + y
        y += 80
    backButton = Button(backButtonFunction, text = 'Back', x = 770, 
                        y = app.height - 50, selectFun = False)
    buttonList.append(backButton)
    return buttonList

def level_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'level', mouseX, mouseY)

def level_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'level', mouseX, mouseY)

def level_onMouseMove(app, mouseX, mouseY):
    onButtonMove(app, 'level', mouseX, mouseY)

def level_redrawAll(app):
    img = Image.open(f"images/level_background.png")
    img = CMUImage(img)
    drawBackGround(app, img)
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
    resetButton = Button(resetButtonFunction, text = 'Reset', width = 80, 
                         x = 780, y = app.height - 150)
    backButton = Button(backButtonFunction, text = 'Back', width = 80, 
                        x = 780, y = app.height - 90, selectFun = False)
    buttonList = [resetButton, backButton]
    return buttonList

def help_onMousePress(app, mouseX, mouseY):
    onButtonPress(app, 'help', mouseX, mouseY)
    for manager in app.helpSlimeManager:
        manager.mousePressSlimes(mouseX, mouseY)

def help_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'help', mouseX, mouseY)

def help_onMouseMove(app, mouseX, mouseY):
    onButtonMove(app, 'help', mouseX, mouseY)

def help_onStep(app):
    app.stepCount += 1
    for manager in app.helpSlimeManager:
        for slime in manager.slimeList:
            if not slime.isSelect:
                slime.image = slime.imageList[app.stepCount % 2]
    if app.stepCount == 4:
        app.stepCount = 0

def help_redrawAll(app):
    drawImage(app.helpImg, 0, 0)
    # drawImage(app.wheelImg, app.width/2 + 3 * app.r, app.height/2 - 2 * app.r, 
    #         align = 'center')
    for manager in app.helpSlimeManager:
        manager.drawSlimes()
        manager.drawPair()
    drawButton(app.help_buttonList)
    
#---game_buttons----------------------------------------------------------------

def resetButton(app):
    app.game_buttonList[1].forbidButton()
    app.game_buttonList[2].forbidButton()

def hintButtonFunction(app):
    if app.slimesManager.hint != None and not app.isPause:
        app.hintStatus = not app.hintStatus

def undoButtonFunction(app):
    if app.slimesManager.undoMix != None and not app.isPause:
        app.slimesManager.undo()
        app.game_buttonList[1].forbidButton()
        app.game_buttonList[2].actButton()

def redoButtonFunction(app):
    if app.slimesManager.redoMix != None and not app.isPause:
        app.slimesManager.redo()
        app.game_buttonList[1].actButton()
        app.game_buttonList[2].forbidButton()

def reStartButtonFunction(app):
    loadSlimeManager(app, app.tmpMapList)
    if app.curScreen != 'game':
        app.curScreen = app.prevScreen.pop()
        setActiveScreen(app.curScreen)
        resetButton(app)

def pauseButtonFunction(app):
    app.isPause = not app.isPause
    if app.isPause:
        app.game_buttonList[4].text = 'Continue'
        # screenManage(app, 'help')
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
    undoButton = Button(undoButtonFunction, 'Undo')
    redoButton = Button(redoButtonFunction, 'Redo')
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
        x += 120
    return buttonList

def game_onMousePress(app, mouseX, mouseY):
    if not app.isPause:
        app.status = app.slimesManager.mousePressSlimes(mouseX, mouseY)
        if app.status == 'win' or app.status == 'lose':
            loadGrading(app)
            screenManage(app, 'evaluate')
        if app.slimesManager.undoMix != None:
            app.game_buttonList[1].actButton()
        if app.slimesManager.redoMix == None:
            app.game_buttonList[2].forbidButton()
    onButtonPress(app, 'game', mouseX, mouseY)

def game_onMouseRelease(app, mouseX, mouseY):
    onButtonRelease(app, 'game', mouseX, mouseY)

def game_onMouseMove(app, mouseX, mouseY):
    onButtonMove(app, 'game', mouseX, mouseY)

def game_onStep(app):
    app.stepCount += 1
    if app.stepCount == 4:
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
        app.stepCount = 0
    if not app.slimesManager.mixLegal and not app.isPause:
        app.remindTime -= 1
        if app.remindTime == 0:
            app.slimesManager.mixLegal = True
            app.remindTime = 3
    for slime in app.slimesManager.slimeList:
        if not slime.isSelect:
            slime.image = slime.imageList[app.stepCount % 2]

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
    # if app.isPause:
    #     pass
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
    backButton = Button('welcome', 'Back', app.width/2 + 60, 
                        app.height/2 + 2.5*app.r, selectFun = False)
    reStartButton = Button(reStartButtonFunction, 'Restart', app.width/2 - 60, 
                           app.height/2 + 2.5*app.r, selectFun = False)
    buttonList = [backButton, reStartButton]
    return buttonList

def evaluate_onStep(app):
    app.stepCount += 1
    for slime in app.evaluateSlimeList:
        slime.image = slime.imageList[app.stepCount % 2]
    if app.stepCount == 4:
        app.stepCount = 0

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

def evaluate_onMouseMove(app, mouseX, mouseY):
    onButtonMove(app, 'evaluate', mouseX, mouseY)

def main():
    runApp()

runAppWithScreens(initialScreen='welcome')