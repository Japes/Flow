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
import fallingBoxesLayer
import hitBoxesLayer


class MonkSprite(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(MonkSprite, self).__init__('assets/monk1.png')
        self.position = x,y
        
class MonkLayer(cocos.layer.Layer):
    def __init__(self):
        super(MonkLayer, self).__init__()
        self.add(MonkSprite(g.screenWidth/2, g.screenHeight/2))


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**g.consts['window'])

    main_scene = cocos.scene.Scene(cocos.layer.ColorLayer(64, 64, 224, 255))

    monk_layer = MonkLayer()
    main_scene.add(monk_layer)

    hitbox_layer = hitBoxesLayer.HitBoxesLayer()
    main_scene.add(hitbox_layer)

    fallingBoxes_layer = fallingBoxesLayer.FallingBoxesLayer()
    main_scene.add(fallingBoxes_layer)

    cocos.director.director.run(main_scene)

