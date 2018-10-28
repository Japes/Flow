from __future__ import division, print_function, unicode_literals

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.scenes import *
import cocos.audio.pygame.mixer

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
        #print(str(self.s.currentLevel))

        #limit speed, check for death
        maxSpeed = 15
        minSpeed = -15
        self.s.currentSpeed = min(self.s.currentSpeed, maxSpeed)
        self.s.currentSpeed = max(self.s.currentSpeed, minSpeed)

        #update level based on speed
        self.s.currentLevel += self.s.currentSpeed
        self.s.currentLevel = max(0, self.s.currentLevel)
        if(self.s.currentLevel == 0):
            self.s.currentSpeed = max(0, self.s.currentSpeed) #can't sink lower

        #difficulty curve
        if(self.s.currentLevel < g.script_startflying ) :
            #print("lvl1")
            self.fallingBoxes_layer.maxBPS = 1
            self.fallingBoxes_layer.ratioSkips = 0.0
            self.fallingBoxes_layer.ratioInbetweeners = 0
        elif(self.s.currentLevel < g.script_2 ) :
            #print("lvl2")
            self.fallingBoxes_layer.maxBPS = 1
            self.fallingBoxes_layer.ratioSkips = 0.0
            self.fallingBoxes_layer.ratioInbetweeners = 0.20
        elif(self.s.currentLevel < g.script_3 ) :
            #print("lvl3")
            self.fallingBoxes_layer.maxBPS = 1
            self.fallingBoxes_layer.ratioSkips = 0.2
            self.fallingBoxes_layer.ratioInbetweeners = 0.25
        elif(self.s.currentLevel < g.script_4 ) :
            #print("lvl4")
            self.fallingBoxes_layer.maxBPS = 1
            self.fallingBoxes_layer.ratioSkips = 0.3
            self.fallingBoxes_layer.ratioInbetweeners = 0.45
        elif(self.s.currentLevel < g.script_5 ) :
            #print("lvl5")
            self.fallingBoxes_layer.maxBPS = 2
            self.fallingBoxes_layer.ratioSkips = 0
            self.fallingBoxes_layer.ratioInbetweeners = 0
        elif(self.s.currentLevel < g.script_win ) :
            #print("lvl6")
            self.fallingBoxes_layer.maxBPS = 2
            self.fallingBoxes_layer.ratioSkips = 0.2
            self.fallingBoxes_layer.ratioInbetweeners = 0.2

        #win condition
        if((not self.s.haveWon) and self.s.currentLevel > g.script_win):
            self.s.haveWon = True
            self.monk_layer.win()
            #we just let the player carry on playing.

        #"lose condition"
        if(time.time() - self.s.timeLastKeyPress > 10 ):
            cocos.director.director.replace( FadeTransition( MainScene(), 2))
            self.unschedule(self.update)

if __name__ == "__main__":
    cocos.audio.pygame.mixer.init()
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**g.consts['window'])
    cocos.director.director.run( FadeTransition( MainScene(), 3, cocos.scene.Scene(cocos.layer.ColorLayer(255, 255, 255, 255))) )

