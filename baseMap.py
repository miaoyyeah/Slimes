from baseSlimes import BaseSlimes
import math

#---baseMap class---------------------------------
# store baseMap object
# store baseGrid
class BaseMap:
    gridDict = {7: "hexGrid", 10: "triGrid", 13: "starGrid"}
    counterDict = {7: 40, 10: 60, 13: 90}

    def __init__(self, indexList, x, y, d, h, rows, cols):
        self.indexList = indexList
        
        if len(indexList) in BaseMap.gridDict:
            gridType = BaseMap.gridDict[len(indexList)]
            self.counter = BaseMap.counterDict[len(indexList)]
        else:
            gridType = 'rectGrid'
            self.counter = 0

        self.posList = getattr(BaseMap, gridType)(x, y, d, h, rows, cols)
        # math.ceil(len(indexList)/2*5)

        self.level = (len(indexList) - 7)//3 + 1

    def __hash__(self):
        return hash(str(self))

    def hexGrid(x, y, d, h, rows, cols):
        posList =  [(x - d/2, y - h), (x + d/2, y - h),
                    (x - d, y), (x, y), (x + d, y),
                    (x - d/2, y + h), (x + d/2, y + h)]
        return posList
    
    def triGrid(x, y, d, h, rows, cols):
        posList = BaseMap.hexGrid(x, y, d, h, rows, cols)
        posList.insert(0, (x, y - 2*h))
        posList.insert(6, (x - 3*d/2, y + h))
        posList.append((x + 3*d/2, y + h))
        return posList
    
    def starGrid(x, y, d, h, rows, cols):
        posList = BaseMap.triGrid(x, y, d, h, rows, cols)
        posList.insert(1, (x - 3 * d/2, y - h))
        posList.insert(4, (x + 3 * d/2, y - h))
        posList.append((x, y + 2*h))
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
