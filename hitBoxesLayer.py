import cocos
import cocos.actions as ac
from cocos.sprite import Sprite

import flowglobals as g

spriteScale = 0.75

class HitBoxSprite(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(HitBoxSprite, self).__init__('assets/circle.png', scale=spriteScale)
        self.position = x,y

class HitBoxesLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(HitBoxesLayer, self).__init__()
        self.hitBoxes = []
        for pos in g.hitBoxPositions:
            sprite = HitBoxSprite(pos, g.hitBoxHeight)
            self.add(sprite)
            self.hitBoxes.append(sprite)

    def on_key_press (self, k, modifiers):
        if (k in g.keyBindings):
            hitbox = self.hitBoxes[g.keyBindings.index(k)]
            hitbox.do(ac.ScaleTo(spriteScale*1.2, 0.05) + ac.ScaleTo(spriteScale, 0.1))