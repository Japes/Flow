from __future__ import division, print_function, unicode_literals

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.scenes import *

#other stuff
import random
import time

#my stuff
import flowglobals as g
import backgroundLayer
import fallingBoxesLayer
import hitBoxesLayer
import monkLayer

class State():
    def __init__(self):
        self.currentSpeed = 0 #speed at which you are ascending (in pixels per frame)
        self.currentLevel = 0 #position along the path to enlightenment
        self.haveWon = False
        self.timeLastKeyPress = time.time()

class MainScene(cocos.scene.Scene):
    def __init__(self):
        super(MainScene, self).__init__()

        self.s = State()
        self.background_Layer = backgroundLayer.BackgroundLayer(self.s)
        self.add(self.background_Layer)
        
        self.monk_layer = monkLayer.MonkLayer(self.s)
        self.add(self.monk_layer)

        self.hitbox_layer = hitBoxesLayer.HitBoxesLayer()
        self.add(self.hitbox_layer)

        self.fallingBoxes_layer = fallingBoxesLayer.FallingBoxesLayer(self.s)
        self.add(self.fallingBoxes_layer)

        self.reset()
        self.schedule(self.update)

    def reset(self):
        self.s.currentSpeed = 0
        self.s.currentLevel = 0

    #main game logic loop
    def update(self, dt):
        print(str(self.s.currentLevel))

        #limit speed, check for death
        maxSpeed = 15
        minSpeed = -45
        self.s.currentSpeed = min(self.s.currentSpeed, maxSpeed)
        self.s.currentSpeed = max(self.s.currentSpeed, minSpeed)

        #update level based on speed
        self.s.currentLevel += self.s.currentSpeed
        self.s.currentLevel = max(0, self.s.currentLevel)
        if(self.s.currentLevel == 0):
            self.s.currentSpeed = max(0, self.s.currentSpeed) #can't sink lower

        #win condition
        if((not self.s.haveWon) and self.s.currentLevel > 10000):
            self.s.haveWon = True
            self.monk_layer.win()
            #we just let the player carry on playing.

        #"lose condition"
        if(time.time() - self.s.timeLastKeyPress > 10 ):
            cocos.director.director.replace( FadeTransition( MainScene(), 2))
            self.unschedule(self.update)

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**g.consts['window'])
    cocos.director.director.run( FadeTransition( MainScene(), 3, cocos.scene.Scene(cocos.layer.ColorLayer(255, 255, 255, 255))) )

