from cmu_graphics import *
from PIL import Image

#---Button class---------------------------------
class Button:    
    def __init__(self, fun, text = None, x = 0, y = 0, width = 100, height = 50, 
                 border = "black", fill = 'papayaWhip', selectFun = True, 
                 imgNameList = ['default', 'press', 'move']):
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

        self.imgNameList = imgNameList
        self.loadButtonImg()
        self.img = self.imgList[0]

    def loadButtonImg(self):
        self.imgList = []
        for name in self.imgNameList:
            image = Image.open(f"images/button/button_{name}.png")
            if self.width != 100:
                image = image.resize((self.width, self.height))
            image = CMUImage(image)
            self.imgList.append(image)
        # if self.imgNameList == Button.defaultImgList:
        #     imgList = Button.defaultImgList
        #     for i in range(len(self.imgNameList)):
        #         image = imgList[i].resize((self.width, self.height))
        #         image = CMUImage(image)
        #         self.imgList.append(image)
        # else:
        #     for name in self.imgNameList:
        #         image = Image.open(f"images/button/button_{name}.png")
        #         image = image.resize((self.width, self.height))
        #         image = CMUImage(image)
        #         self.imgList.append(image)

    def onMousePressButton(self):
        if self.img != self.imgList[1]:
            self.img = self.imgList[1]
        if not isinstance(self.fun, str):
            if self.selectFun:
                self.fun(app)
            return None

    def onMouseReleaseButton(self):
        self.img = self.imgList[0]
        if isinstance(self.fun, str):
            return self.fun
        else:
            self.fun(app)
            return None
    
    def onMouseMoveButton(self, mouseX, mouseY):
        if self.img != self.imgList[1]:
            if self.checkForPress(mouseX, mouseY):
                self.img = self.imgList[2]
            else:
                self.img = self.imgList[0]

    def draw(self):
        drawImage(self.img, self.x, self.y, align = 'center')
        # drawRect(self.x, self.y, self.width, self.height, fill = self.fill, 
        #          align = 'center', border = self.border)
        if self.text != None:
            drawLabel(self.text, self.x, self.y, size = 20)

    def checkForPress(self, mouseX, mouseY):
        return (self.x - self.width/2 < mouseX < self.x + self.width/2 and 
            self.y - self.height/2 < mouseY < self.y + self.height/2)
    
    def forbidButton(self):
        self.img = self.imgList[1]

    def actButton(self):
        self.img = self.imgList[0]
