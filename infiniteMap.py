from baseMap import BaseMap

class InfiniteMap(BaseMap):
    def infinitePosList(n, x, y, d, h):
        i = 1
        posList = []
        Vector = [(-d / 2, h), (-d, 0), (-d / 2, -h), 
                (d / 2, -h), (d, 0), (d / 2, h)]
        y0 = y
        posList.append(((x, y)))
        k0 = 1
        while i < n:
            for j in range(6):
                k = 0
                while k < k0:
                    if i < n:
                        if k == k0 - 1 and j == 1:
                            break
                        dx, dy = Vector[j]
                        x += dx
                        y += dy
                        if abs(y - y0) < 2.1 * h:
                            posList.append((x, y))
                            i += 1
                    k += 1
            k0 += 1
        return posList

    def __init__(self, indexList, x, y, d, h, rows = 0, cols = 0):
        self.indexList = indexList
        self.counter = 60
        n = len(indexList)
        self.posList = InfiniteMap.infinitePosList(n, x, y, d, h)
        self.level = 0