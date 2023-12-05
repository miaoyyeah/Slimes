from cmu_graphics import *
from PIL import Image
from baseSlimes import BaseSlimes
import copy

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

#---SlimesManager class---------------------------------------------------------
class SlimesManager:
    def loadSlimeList(map):
        slimeList = []
        for pos in range(len(map.posList)):
                x, y = map.posList[pos]
                slimeList.append(BaseSlimes(map.indexList[pos], x, y))
        return slimeList

    def __init__(self, map):
        self.slimeList = SlimesManager.loadSlimeList(map)
        self.indexPair = []
        self.score = 0
        self.hint = self.canSolve(map.indexList)[:2]
        self.prevHint = self.hint
        self.slimeCount = self.loadSlimeCount()
        self.undoMix = None
        self.redoMix = None
        self.mixLegal = True
        image = Image.open(f"images/remind.png")
        image = image.resize((260, 80))
        self.remindImg = CMUImage(image)

    def loadSlimeCount(self):
        slimeCount = dict()
        for index in range(6):
            slimeCount[index] = 0
        return slimeCount
    
    #---canSolve methods--------------------------------------------------------
    
    def canSolve(self, indexList):
        return self.solveHelper(copy.copy(indexList), [], [])

    def solveHelper(self, remainL, numPair, solL):
        if remainL == []:
            return solL
        else:
            for i in range(len(remainL)):
                nextNum = remainL[i]
                if self.canMix(nextNum, numPair):
                    newNumPair = numPair + [nextNum]
                    newNumL = []
                    if len(newNumPair) == 2:
                        newNumL = self.manageNumPair(newNumPair)
                        newNumPair = []
                    newRemainL = remainL[:i] + remainL[i + 1:] + newNumL
                    newSolL = solL + [remainL[i]]
                    sol = self.solveHelper(newRemainL, newNumPair, newSolL)
                    if sol != None:
                        return sol
            return None

    def canMix(self, num, numPair):
        if len(numPair) < 1 or num == numPair[0]:
            return True
        else:
            dif = abs(num - numPair[0])
            return dif == 0 or dif == 2 or dif == 4

    def manageNumPair(self, numPair):
        dif = abs(numPair[0] - numPair[1])
        sum = abs(numPair[0] + numPair[1])
        if dif == 0:
            return []
        elif dif == 2:
            newNum = int(sum / 2)
        elif sum == 4:
            newNum = int((sum + 6)/2)
        elif sum == 6:
            newNum = int((sum - 6)/2)
        return [newNum]
    
    #---SlimesMix methods-------------------------------------------------------
    def mousePressSlimes(self, mouseX, mouseY):
        index = self.clickSlimesIndex(mouseX, mouseY)
        if index != None:
            length = len(self.indexPair)
            if length == 0:
                self.indexPair.append(index)
            elif length == 1 and index != self.indexPair[0]:
                self.indexPair.append(index)
                status = self.mixSlimes()
                if status:
                    return self.canSlimeSolve()
                else:
                    self.mixLegal = False
            else:
                self.clearPair()
        else:
            self.clearPair()
        return None
    
    # check if mouse click on one slime
    # if on one slime: return the slime name index
    # else: return None
    def clickSlimesIndex(self, mouseX, mouseY):
        for i in range(len(self.slimeList)):
            slime = self.slimeList[i]
            dist = distance(slime.x, slime.y, mouseX, mouseY)
            if dist <= slime.r/2:
                # pixel = slime.image.image.getpixel((mouseX, mouseY))
                # print(pixel)
                return i
        return None

    # if dif == 2 or 4: mix
    # elif dif == 0: remove
    def mixSlimes(self):
        if self.indexPair[0] == self.indexPair[1]:
            self.clearPair()
            return
        index1, index2 = self.indexPair[0], self.indexPair[1]
        slimeList = self.slimeList
        slime1, slime2 = slimeList[index1], slimeList[index2]
        
        dif = abs(slime1.index - slime2.index)
        sum = abs(slime1.index + slime2.index)

        if dif == 2 or dif == 4:
            if dif == 2:
                newIndex = int((sum)/2)
            elif sum == 4:
                newIndex = int((sum + 6)/2)
            elif sum == 6:
                newIndex = int((sum - 6)/2)

            newSlime = BaseSlimes(newIndex, slime2.x, slime2.y)
            self.undoMix = [slime1, slime2, newSlime]
            slimeList.append(newSlime)
            self.managePair()
            return True

        elif dif == 0:
            self.undoMix = [slime1, slime2]
            self.managePair()
            return True
        
        else:
            self.clearPair()
            return False
    
    def managePair(self):
        slimesPair = [self.slimeList[self.indexPair[0]], 
                      self.slimeList[self.indexPair[1]]]
        for slime in slimesPair:
            self.slimeCount[slime.index] += 1
            self.slimeList.remove(slime)
            self.score += slime.value
            self.isSelect = False
        self.indexPair = []
        self.redoMix = None
    
    def clearPair(self):
        for i in self.indexPair:
            self.slimeList[i].isSelect = False
        self.indexPair = []

    def canSlimeSolve(self):
        if self.slimeList == []:
            return 'win'
        indexList = []
        for slime in self.slimeList:
            indexList.append(slime.index)
        solL = self.canSolve(indexList)
        if solL == None:
            return 'lose'
        else:
            self.hint = solL[:2]

    def undo(self):
        if self.undoMix != None:
            self.redoMix = copy.copy(self.undoMix)
            if len(self.undoMix) == 3:
                self.slimeList.remove(self.undoMix.pop())
            for slime in self.undoMix:
                self.slimeList.append(slime)
                self.score -= slime.value
            tmpHint = self.hint
            self.hint = self.prevHint
            self.prevHint = tmpHint
            self.undoMix = None
    
    def redo(self):
        if self.redoMix != None:
            self.undoMix = copy.copy(self.redoMix)
            if len(self.redoMix) == 3:
                self.slimeList.append(self.redoMix.pop())
            for slime in self.redoMix:
                self.score += slime.value
                self.slimeList.remove(slime)
            tmpHint = self.hint
            self.hint = self.prevHint
            self.prevHint = tmpHint
            self.redoMix = None

    #---draw methods------------------------------------------------------------

    def drawSlimes(self):
        for slime in self.slimeList:
            slime.draw()
    
    def drawPair(self):
        if len(self.indexPair) == 1:
            i = self.indexPair[0]
            self.slimeList[i].isSelect = True
            self.slimeList[i].image = self.slimeList[i].imageList[1]
            # x, y = self.slimeList[i].x, self.slimeList[i].y
            # r = 0.2 * self.slimeList[i].r
            # drawCircle(x, y, r, border = 'red', fill = None)
        elif len(self.indexPair) == 2:
            for i in self.indexPair:
                self.slimeList[i].isSelect = False

    def drawHint(self):
        indexList = []
        for slime in self.slimeList:
            indexList.append(slime.index)
        for i in self.hint:
            if i in indexList:
                index = indexList.index(i)
                slime = self.slimeList[index]
                x = slime.x
                y = slime.y
                r = 0.2 * slime.r
                drawCircle(x, y, r, border = 'white', fill = None)
                indexList[index] = -1
    
    def drawRemind(self):
        drawImage(self.remindImg, 450, 310, align = 'center')
        drawLabel("YOU CAN'T MIX THEM!", 450, 315, size = 20)
