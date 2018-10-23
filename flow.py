from __future__ import division, print_function, unicode_literals

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key

#other stuff
import random

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

g_screenHeight = consts["window"]["height"]
g_screenWidth = consts["window"]["width"]
g_hitBoxHeight = g_screenHeight/5

g_keyBindings =     [key.LEFT,          key.DOWN,           key.RIGHT           ]     # the buttons in order from left to right
g_hitBoxPositions = [g_screenWidth/3,   g_screenWidth/2,    2*g_screenWidth/3   ]     # x coords of hitboxes in order from left to right

class HitBox(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(HitBox, self).__init__('circle.png')
        self.position = x,y

class HitBoxes(cocos.layer.Layer):
    def __init__(self):
        super(HitBoxes, self).__init__()
        for pos in g_hitBoxPositions:
            sprite = HitBox(pos, g_hitBoxHeight)
            self.add(sprite)

class FallingBox(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(FallingBox, self).__init__('circle.png')
        self.position = x,y
        action = ac.MoveTo((self.position[0], -consts["window"]["height"]*1.25), 8)
        self.do(action)

class FallingBoxes(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(FallingBoxes, self).__init__()
        self.schedule_interval(self.generateBox, 1)
        self.boxes = []
        for col in g_keyBindings:
            self.boxes.append([])

        self.text = cocos.text.Label("", x=100, y=280)
        self.add(self.text)

    #called by scheduler
    def generateBox(self, dt):
        random_index = random.randrange(len(g_keyBindings))
        sprite = FallingBox(g_hitBoxPositions[random_index], consts["window"]["height"]*1.25)
        self.add(sprite)
        self.boxes[random_index].append(sprite)

    def on_key_press (self, k, modifiers):
        if (k in g_keyBindings):
            children = self.boxes[g_keyBindings.index(k)]
            bestOne = min([abs(child.y - g_hitBoxHeight) for child in children])
            self.text.element.text = str(bestOne)
            bestChild = [child for child in children if abs(child.y - g_hitBoxHeight) == bestOne][0] #yuck
            if(bestChild and bestOne < 10):
                action = ac.FadeOut(0.25) + ac.CallFuncS(self.remove_child)
                bestChild.do(action)

    def remove_child(self, sprite):
        self.remove(sprite)

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

