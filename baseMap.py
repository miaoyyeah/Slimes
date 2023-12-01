from baseSlimes import BaseSlimes
import math

#---baseMap class---------------------------------
# store baseMap object
# store baseGrid
class BaseMap:
    def __init__(self, indexList, gridType, x, y, d, h, rows, cols):
        self.indexList = indexList
        self.gridType = gridType
        self.posList = getattr(BaseMap, gridType)(x, y, d, h, rows, cols)
        self.counter = 60
        # math.ceil(len(indexList)/2*5)
        self.level = math.floor((len(indexList) + len(set(indexList)))/8)

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
#------------------------------------
def getIndexList(mapName):
    mapName = f'{mapName}_indexList'
    return globals()[mapName]

slimeName = BaseSlimes.getSlimeName()
baseMap1_nameList = [slimeName[0], slimeName[0],
                     slimeName[3], slimeName[4], slimeName[5],
                     slimeName[2], slimeName[2]]
baseMap1_indexList = [0, 0, 3, 4, 5, 2, 2]
