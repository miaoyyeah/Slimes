from cmu_graphics import *
from PIL import Image

#---Button class---------------------------------
class Button:
    def __init__(self, name, link, x = 0, y = 0, width = 200, height = 50, 
                 border = "black", fill = 'papayaWhip'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border

        self.fill = fill
        self.pressFill = 'lightGray'
        self.isPress = False

        self.name = name
        self.link = link
    
    def __hash__(self):
        return hash(str(self))

    def onMousePressButton(self, mouseX, mouseY):
        if (self.x - self.width/2 < mouseX < self.x + self.width/2 and 
            self.y - self.height/2 < mouseY < self.y + self.height/2):
            self.isPress = True
            print(self.isPress)
    
    def onMouseReleaseButton(self, mouseX, mouseY):
        if (self.x - self.width/2 < mouseX < self.x + self.width/2 and 
            self.y - self.height/2 < mouseY < self.y + self.height/2):
            self.isPress = False
            print(self.isPress)
            return self.link
        return None

    def draw(self):
        if self.isPress == True:
            drawRect(self.x, self.y, self.width, self.height, align = 'center', 
                 border = self.border, fill = self.pressFill)
        else:
            drawRect(self.x, self.y, self.width, self.height, align = 'center', 
                     border = self.border, fill = self.fill)
        drawLabel(self.name, self.x, self.y, size = 20)
    
    def repr(self):
        return str(self.name)

