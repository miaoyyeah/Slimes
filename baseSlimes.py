from cmu_graphics import *
from PIL import Image

#---baseSlimes class---------------------------------
class BaseSlimes:
    slimeName = ['red', 'yellow', 'green', 'blue', 'purple', 'orchid']
    slimeValue = {'red': 30, 'yellow': 40, 'green': 20, 
                'blue': 30, 'purple': 20, 'orchid': 40}

    def getSlimeName():
        return BaseSlimes.slimeName
    
    def getSlimeValue(name):
        return BaseSlimes.slimeValue[name]

    def __init__(self, index, x = 0, y = 0, r = 88, status = 'move'):
        self.x = x
        self.y = y
        self.r = r

        self.isSelect = False
        self.index = index
        self.name = BaseSlimes.slimeName[index]
        self.value = BaseSlimes.slimeValue[self.name]

        imgName = ['slime', 'flat', 'baseSlime']
        self.imageList = []
        for name in imgName:
            image = Image.open(f"images/baseSlime/{name}_{self.name}.png")
            if r != 88:
                image = self.image.resize((r, r))
            image = CMUImage(image)
            self.imageList.append(image)
        self.image = self.imageList[1]

        self.status = 'move'
    
    def __hash__(self):
        return hash(str(self.index) + str(self.name))

    def draw(self):
        drawImage(self.image, self.x, self.y, align = 'center')
    
    def repr(self):
        return str(self.name)


