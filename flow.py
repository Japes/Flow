from __future__ import division, print_function, unicode_literals

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key

#other stuff
import random

#my stuff
import flowglobals as g
import backgroundLayer
import fallingBoxesLayer
import hitBoxesLayer
import monkLayer

class MainScene(cocos.scene.Scene):
    def __init__(self):
        super(MainScene, self).__init__()

        self.background_Layer = backgroundLayer.BackgroundLayer()
        self.add(self.background_Layer)

        self.monk_layer = monkLayer.MonkLayer()
        self.add(self.monk_layer)

        self.hitbox_layer = hitBoxesLayer.HitBoxesLayer()
        self.add(self.hitbox_layer)

        self.fallingBoxes_layer = fallingBoxesLayer.FallingBoxesLayer()
        self.add(self.fallingBoxes_layer)
        
        self.schedule(self.update)

    def update(self, dt):
        if(g.currentSpeed > 15):
            g.currentSpeed = 15
        if(g.currentSpeed < -45):
            g.currentSpeed = -45

        #win condition
        if(g.currentLevel > 1000):
            self.monk_layer.win()

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**g.consts['window'])

    main_scene = MainScene()
    cocos.director.director.run(main_scene)

