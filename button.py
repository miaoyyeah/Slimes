from cmu_graphics import *
from PIL import Image

#---Button class---------------------------------
class Button:
    def __init__(self, fun, text = None, x = 0, y = 0, width = 200, height = 50, 
                 border = "black", fill = 'papayaWhip'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border

        self.fill = fill
        self.selectedFill = 'lightGray'
        self.selected = False

        self.text = text
        self.fun = fun
    
    def onMousePressButton(self, mouseX, mouseY):
        if self.checkForPress(mouseX, mouseY):
            self.selected = True
            if not isinstance(self.fun, str):
                self.fun(app)
                return None

    def onMouseReleaseButton(self, mouseX, mouseY):
        self.selected = False
        if self.checkForPress(mouseX, mouseY):
            print(self.text)
            if isinstance(self.fun, str):
                return self.fun
            else:
                self.fun(app)
                return None

    def draw(self):
        if self.selected:
            fill = self.selectedFill
        else:
            fill = self.fill
        drawRect(self.x, self.y, self.width, self.height, fill = fill, 
                 align = 'center', border = self.border)
        if self.text != None:
            drawLabel(self.text, self.x, self.y, size = 20)

    def checkForPress(self, mouseX, mouseY):
        return (self.x - self.width/2 < mouseX < self.x + self.width/2 and 
            self.y - self.height/2 < mouseY < self.y + self.height/2)