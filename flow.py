from __future__ import division, print_function, unicode_literals

import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key

consts = {
    "window": {
        "width": 800,
        "height": 600,
        "vsync": True,
        "resizable": True
    },
    "world": {
        "width": 400,
        "height": 300,
        "rPlayer": 8.0,
        "wall_scale_min": 0.75,  # relative to player
        "wall_scale_max": 2.25,  # relative to player
        "topSpeed": 100.0,
        "angular_velocity": 240.0,  # degrees / s
        "accel": 85.0,
        "bindings": {
            key.LEFT: 'left',
            key.RIGHT: 'right',
            key.UP: 'up',
        }
    },
    "view": {
        # as the font file is not provided it will decay to the default font;
        # the setting is retained anyway to not downgrade the code
        "font_name": 'Axaxax',
        "palette": {
            'bg': (0, 65, 133),
            'player': (237, 27, 36),
            'wall': (247, 148, 29),
            'gate': (140, 198, 62),
            'food': (140, 198, 62)
        }
    }
}

g_hitBoxHeight = consts["window"]["height"]/5


class HitBox(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(HitBox, self).__init__('circle.png')
        self.position = x,y

class HitBoxes(cocos.layer.Layer):
    def __init__(self):
        super(HitBoxes, self).__init__()
        sprite = HitBox(consts["window"]["width"]/2, g_hitBoxHeight)
        self.add(sprite)
        #spriteWidth = sprite.get_rect().size[0]

class FallingBox(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(FallingBox, self).__init__('circle.png')
        self.position = x,y
        action = ac.MoveTo((self.position[0], -consts["window"]["height"]*1.25), 8)
        self.do(action)

class FallingBoxes(cocos.layer.Layer):
    is_event_handler = True
    boxes = set()


    def __init__(self):
        super(FallingBoxes, self).__init__()
        self.schedule_interval(self.update, 1)
        self.text = cocos.text.Label("", x=100, y=280)
        self.add(self.text)

    def update(self, dt):
        
        sprite = FallingBox(consts["window"]["width"]/2, consts["window"]["height"]*1.25)
        self.add(sprite)

    def on_key_press (self, k, modifiers):
        if (k == key.DOWN):
            children = self.get_children()
            bestOne = min([abs(child.y - g_hitBoxHeight) for child in children])
            self.text.element.text = str(bestOne)
            bestChild = [child for child in children if abs(child.y - g_hitBoxHeight) == bestOne] #yuck
            if(bestChild and bestOne < 10):
                self.remove(bestChild[0])


if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(**consts['window'])

    #layers
    background_layer = cocos.layer.ColorLayer
    fallingBoxes_layer = FallingBoxes()
    hitbox_layer = HitBoxes()

    #scene
    main_scene = cocos.scene.Scene(cocos.layer.ColorLayer(64, 64, 224, 255))
    main_scene.add(hitbox_layer)
    main_scene.add(fallingBoxes_layer)

    cocos.director.director.run(main_scene)

