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

    def __init__(self, name, x = 0, y = 0, r = 100):
        self.x = x
        self.y = y
        self.r = r

        self.name = name
        self.index = BaseSlimes.slimeName.index(name)
        self.value = BaseSlimes.slimeValue[name]

        self.image = Image.open(f"images/baseSlime/baseSlime_{name}.png")
        self.image = self.image.resize((r, r))
        self.image = CMUImage(self.image)
    
    def __hash__(self):
        return hash(str(self.index) + str(self.name))

    def draw(self):
        drawImage(self.image, self.x, self.y, align = 'center')
    
    def repr(self):
        return str(self.name)


