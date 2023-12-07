import random
import copy

def generatePair(indexList):
    index = random.randint(0, 5)
    indexList.append(index)
    indexList.append(index)

def split(indexList):
    splitIndex = indexList[random.randint(0, len(indexList) - 1)]
    if splitIndex == 0:
        newIndexPair = [1, 5]
    elif splitIndex == 5:
        newIndexPair = [0, 4]
    else:
        newIndexPair = [splitIndex - 1, splitIndex + 1]
    indexList.remove(splitIndex)
    indexList.extend(newIndexPair)

def generateMap(n, sort = True):
    indexList = []
    generatePair(indexList)
    # print(indexList)
    while len(indexList) < n - 1:
        generateOption = random.randint(0, 1)
        if generateOption == 0:
            generatePair(indexList)
            # print(indexList)
        else:
            split(indexList)
            # print(indexList)
    if len(indexList) + 1 == n:
        split(indexList)
        # print(indexList)
    if sort:
        indexList.sort()
    else:
        random.shuffle(indexList)
    return indexList
