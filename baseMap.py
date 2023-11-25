from baseSlimes import BaseSlimes
import math

#---baseMap class---------------------------------
# store baseMap object
# store baseGrid
class BaseMap:
    def __init__(self, nameList, gridType, x, y, d, h, rows, cols):
        self.nameList = nameList
        self.gridType = gridType
        self.posList = getattr(BaseMap, gridType)(x, y, d, h, rows, cols)
        self.counter = math.ceil(len(nameList)/2*5)
        self.level = math.floor((len(nameList) + len(set(nameList)))/8)

    def __hash__(self):
        return hash(str(self))

    def hexGrid(x, y, d, h, rows, cols):
        posList =  [(x - d/2, y - h), (x + d/2, y - h),
                    (x - d, y), (x, y), (x + d, y),
                    (x - d/2, y + h), (x + d/2, y + h)]
        return posList
    
    def rectGrid(x, y, d, h, rows, cols):
        posList = []
        for row in range(rows):
            for col in range(cols):
                posList.append((x + col * d, y + row * h))
        return posList
    
    def helpGrid(x, y, r):
        d = 0.5*r
        posList = []
        for i in range(2):
            posList.append((x + i * d, y))
        return posList

#---baseMap objects---------------------------------
def getNameList(mapName):
    mapName = f'{mapName}_nameList'
    return globals()[mapName]

slimeName = BaseSlimes.getSlimeName()
baseMap1_nameList = [slimeName[0], slimeName[0],
                     slimeName[3], slimeName[4], slimeName[5],
                     slimeName[2], slimeName[2]]