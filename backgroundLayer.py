#other stuff

#cocos stuff
import cocos
from cocos.sprite import Sprite
import cocos.actions as ac

#my stuff
import flowglobals as g

updateInterval = 0.2

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.backgroundSprites = [Sprite('assets/background.jpg', scale=2), Sprite('assets/background2.jpg', scale=2), Sprite('assets/background3.jpg', scale=2)]
        self.schedule_interval(self.updateSpeed, updateInterval)
        self.schedule(self.update)

        self.backgroundSprites[0].position = g.screenWidth/2, g.screenHeight/2
        self.setCurrentSprite(self.backgroundSprites[0])

    #called by scheduler
    def updateSpeed(self, dt):
        move = ac.MoveBy((0, -g.currentSpeed), duration=updateInterval)
        self.currentSprite.do(move)
        self.prevSpr.do(move)
        self.nextSpr.do(move)

    def update(self, dt):
        g.currentLevel = -(self.currentSprite.y)

        if(abs(self.nextSpr.y - g.screenHeight/2) < abs(self.currentSprite.y - g.screenHeight/2)) :
            self.setCurrentSprite(self.nextSpr)

        if(abs(self.prevSpr.y - g.screenHeight/2) < abs(self.currentSprite.y - g.screenHeight/2)) :
            self.setCurrentSprite(self.prevSpr)

        #global game logic which probably doesn't belong here (but this is a convenient update loop):
        if(g.currentSpeed > 15):
            g.currentSpeed = 15
        if(g.currentSpeed < -60):
            g.currentSpeed = -60

    def setCurrentSprite(self, sprite):
        for child in self.get_children():
            self.remove(child)
        self.currentSprite = sprite

        self.nextSpr = self.nextSprite(self.currentSprite)
        self.nextSpr.position = g.screenWidth/2, self.currentSprite.y
        self.nextSpr.y += (self.currentSprite.height*self.currentSprite.scale_y)/2
        self.nextSpr.y += (self.nextSpr.height*self.nextSpr.scale_y)/2

        self.prevSpr = self.prevSprite(self.currentSprite)
        self.prevSpr.position = g.screenWidth/2, self.currentSprite.y
        self.prevSpr.y -= (self.currentSprite.height*self.currentSprite.scale_y)/2
        self.prevSpr.y -= (self.prevSpr.height*self.prevSpr.scale_y)/2

        self.add(self.currentSprite)
        self.add(self.nextSpr)
        self.add(self.prevSpr)
        self.updateSpeed(1)

    def nextSprite(self, sprite):
        index = self.backgroundSprites.index(sprite)
        if (index == len(self.backgroundSprites) - 1) :
            return self.backgroundSprites[0]
        else:
            return self.backgroundSprites[index + 1]
    
    def prevSprite(self, sprite):
        return self.backgroundSprites[self.backgroundSprites.index(sprite) - 1] #could be -1, which is perfect
