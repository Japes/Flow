#other stuff
import random

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key

#my stuff
import flowglobals


class FallingBoxSprite(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(FallingBoxSprite, self).__init__('assets/circle.png')
        self.position = x,y
        action = ac.MoveTo((self.position[0], -flowglobals.consts["window"]["height"]*1.25), 8)
        self.do(action)

class FallingBoxesLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(FallingBoxesLayer, self).__init__()
        self.schedule_interval(self.generateBox, 1)
        self.boxes = []
        for range in flowglobals.keyBindings:
            self.boxes.append([])

        self.text = cocos.text.Label("", x=100, y=280)
        self.add(self.text)

    #called by scheduler
    def generateBox(self, dt):
        random_index = random.randrange(len(flowglobals.keyBindings))
        sprite = FallingBoxSprite(flowglobals.hitBoxPositions[random_index], flowglobals.consts["window"]["height"]*1.25)
        self.add(sprite)
        self.boxes[random_index].append(sprite)

    def on_key_press (self, k, modifiers):
        if (k in flowglobals.keyBindings):
            children = self.boxes[flowglobals.keyBindings.index(k)]
            if(children):
                bestOne = min([abs(child.y - flowglobals.hitBoxHeight) for child in children])
                self.text.element.text = str(bestOne)
                bestChild = [child for child in children if abs(child.y - flowglobals.hitBoxHeight) == bestOne][0] #yuck
                if(bestChild and bestOne < 10):
                    action = ac.FadeOut(0.25) + ac.CallFuncS(self.remove_child)
                    bestChild.do(action)

    def remove_child(self, sprite):
        self.remove(sprite)