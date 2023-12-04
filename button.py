from cmu_graphics import *
from PIL import Image

#---Button class---------------------------------
class Button:
    def __init__(self, fun, text = None, x = 0, y = 0, width = 200, height = 50, 
                 border = "black", fill = 'papayaWhip', selectFun = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.selectFun = selectFun

        self.fillList = [fill, 'lightGray']
        self.fill = self.fillList[0]

        self.text = text
        self.fun = fun
    
    def onMousePressButton(self, mouseX, mouseY):
        self.fill = self.fillList[1]
        if not isinstance(self.fun, str):
            if self.selectFun:
                self.fun(app)
            return None

    def onMouseReleaseButton(self, mouseX, mouseY):
        self.fill = self.fillList[0]
        if isinstance(self.fun, str):
            return self.fun
        else:
            self.fun(app)
            return None

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill = self.fill, 
                 align = 'center', border = self.border)
        if self.text != None:
            drawLabel(self.text, self.x, self.y, size = 20)

    def checkForPress(self, mouseX, mouseY):
        return (self.x - self.width/2 < mouseX < self.x + self.width/2 and 
            self.y - self.height/2 < mouseY < self.y + self.height/2)