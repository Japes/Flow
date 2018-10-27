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
        self.currentSpeed = 0 #speed at which you are ascending
        self.currentLevel = 0 #position along the track

class MainScene(cocos.scene.Scene):
    def __init__(self):
        super(MainScene, self).__init__()

        self.s = State()
        self.background_Layer = backgroundLayer.BackgroundLayer(self.s)
        self.add(self.background_Layer)
        
        self.monk_layer = monkLayer.MonkLayer()
        self.add(self.monk_layer)

        self.hitbox_layer = hitBoxesLayer.HitBoxesLayer()
        self.add(self.hitbox_layer)

        self.fallingBoxes_layer = fallingBoxesLayer.FallingBoxesLayer(self.s)
        self.add(self.fallingBoxes_layer)

        self.reset()
        self.schedule(self.update)

    def reset(self):
        self.minSpeedCounter = 0
        self.s.currentSpeed = 0
        self.s.currentLevel = 0

    def update(self, dt):
        maxSpeed = 15
        minSpeed = -45
        if(self.s.currentSpeed > maxSpeed):
            self.s.currentSpeed = maxSpeed
        elif(self.s.currentSpeed < minSpeed):
            self.s.currentSpeed = minSpeed
            if(self.minSpeedCounter == 0):
                self.minSpeedCounter = time.time()
        elif(minSpeed < self.s.currentSpeed < maxSpeed):
            self.minSpeedCounter = 0 #reset counter

        #win condition
        if(self.s.currentLevel > 1000):
            self.monk_layer.win()
            #maybe just let the player carry on playing?

        #lose condition
        if(self.minSpeedCounter != 0 and time.time() - self.minSpeedCounter > 0 ):
            cocos.director.director.replace( FadeTransition( MainScene(), 2))
            self.unschedule(self.update)

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**g.consts['window'])
    cocos.director.director.run( FadeTransition( MainScene(), 3, cocos.scene.Scene(cocos.layer.ColorLayer(255, 255, 255, 255))) )

