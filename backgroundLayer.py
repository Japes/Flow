#other stuff

#cocos stuff
import cocos
from cocos.sprite import Sprite
import cocos.actions as ac

#my stuff
import flowglobals as g

updateInterval = 0.2

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self, state):
        super(BackgroundLayer, self).__init__()
        self.s = state
        self.currentSpriteStartingPos = 0
        self.accumulatedLevel = 0
        self.currentBackgroundLevel = 0 #absolute scroll position of background.  Not to be confused with state.currentLevel

        self.currentSprite = None
        self.backgroundSprites = [Sprite('assets/background.jpg', scale=2), Sprite('assets/background2.jpg', scale=2), Sprite('assets/background3.jpg', scale=2)]
        self.schedule_interval(self.updateSpeed, updateInterval)
        self.schedule(self.update)

        self.backgroundSprites[0].position = g.screenWidth/2, g.screenHeight/2
        self.setCurrentSprite(self.backgroundSprites[0])


    #called by scheduler
    def updateSpeed(self, dt):
        if(self.s.currentLevel > g.script_startflying):
            self.currentSprite.do(ac.MoveTo((g.screenWidth/2, self.currentSprite.y -self.s.currentSpeed), duration=updateInterval))
            self.prevSpr.do(ac.MoveTo((g.screenWidth/2, self.prevSpr.y -self.s.currentSpeed), duration=updateInterval))
            self.nextSpr.do(ac.MoveTo((g.screenWidth/2, self.nextSpr.y -self.s.currentSpeed), duration=updateInterval))


    def update(self, dt):
        #print("acclev: " + str(self.accumulatedLevel) + " startingPos: " + str(self.currentSpriteStartingPos) + " currentY: " + str(self.currentSprite.y))
        self.currentBackgroundLevel = self.accumulatedLevel + self.currentSpriteStartingPos - self.currentSprite.y
        #print(str(self.s.currentLevel))

        if(abs(self.nextSpr.y - g.screenHeight/2) < abs(self.currentSprite.y - g.screenHeight/2)) :
            self.setCurrentSprite(self.nextSpr)

        if(abs(self.prevSpr.y - g.screenHeight/2) < abs(self.currentSprite.y - g.screenHeight/2)) :
            self.setCurrentSprite(self.prevSpr)

    def setCurrentSprite(self, sprite):
        if(self.currentSprite and sprite != self.currentSprite):
            self.accumulatedLevel = self.currentBackgroundLevel

        for child in self.get_children():
            self.remove(child)
        self.currentSprite = sprite
        self.currentSpriteStartingPos = sprite.y

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
