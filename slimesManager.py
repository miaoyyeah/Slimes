from baseSlimes import BaseSlimes

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

#---SlimesManager class---------------------------------------------------------
class SlimesManager:
    def loadSlimeList(map):
        slimeList = []
        for pos in range(len(map.posList)):
                x, y = map.posList[pos]
                slimeList.append(BaseSlimes(map.nameList[pos], x, y))
        return slimeList
    
    def loadSlimeCount():
        slimeCount = dict()
        nameList = BaseSlimes.getSlimeName()
        for name in nameList:
            slimeCount[name] = 0
        return slimeCount

    def __init__(self, map):
        self.slimeList = SlimesManager.loadSlimeList(map)
        self.slimesPair = []
        self.score = 0
        self.slimeCount = SlimesManager.loadSlimeCount()
    
    #---SlimesMix methods-------------------------------------------------------
    def mousePressSlimes(self, mouseX, mouseY):
        index = self.clickSlimesIndex(mouseX, mouseY)
        if index != None:
            length = len(self.slimesPair)
            slime = self.slimeList[index]
            if length == 0:
                self.slimesPair.append(slime)
            if length == 1 and index != self.slimesPair[0]:
                self.slimesPair.append(slime)
                self.mixSlimes()
        else:
            self.slimePair = []
        if self.slimeList == []:
            return 'win'
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
        slime1, slime2 = self.slimesPair[0], self.slimesPair[1]
        slimeName = BaseSlimes.getSlimeName()
        slimeList = self.slimeList
        
        dif = abs(slime1.index - slime2.index)

        if dif == 2 or dif == 4:
            if dif == 2:
                newIndex = int((slime1.index + slime2.index)/2)
            else:
                newIndex = int((slime1.index + slime2.index + 6)/2)

            newSlime = BaseSlimes(slimeName[newIndex], slime2.x, slime2.y)
            slimeList.append(newSlime)
            self.managePair()
            print(self.score)

        elif dif == 0:
            self.managePair()
            print(self.score)
        
        else:
            self.slimesPair = []
    
    def managePair(self):
        for slime in self.slimesPair:
            self.slimeCount[slime.name] += 1
            self.slimeList.remove(slime)
            self.score += slime.value
        self.slimesPair = []

    def drawSlimes(self):
        for slime in self.slimeList:
            slime.draw()

    

    



