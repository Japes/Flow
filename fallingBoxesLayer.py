#other stuff
import random

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key

#my stuff
import flowglobals as g

spriteScale = 0.75

class FallingBoxSprite(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(FallingBoxSprite, self).__init__('assets/circle.png', scale = spriteScale)
        self.position = x,y
        action = ac.MoveTo((self.position[0], -g.consts["window"]["height"]*1.25), 8)
        self.do(action)
        self.schedule_interval(self.checkForDeath, 0.25)

    def checkForDeath(self, dt):
        if(self.y < -g.screenHeight/10):
            self.kill()
            if(g.currentSpeed > 5):
                g.currentSpeed /= 2
            elif(g.currentSpeed < -5):
                g.currentSpeed *= 2
            else:
                g.currentSpeed -= 10



class FallingBoxesLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(FallingBoxesLayer, self).__init__()
        self.schedule_interval(self.generateBox, 1)
        self.boxes = []
        for range in g.keyBindings:
            self.boxes.append([])

        self.text = cocos.text.Label("", x=100, y=280)
        self.add(self.text)

    #called by scheduler
    def generateBox(self, dt):
        random_index = random.randrange(len(g.keyBindings))
        sprite = FallingBoxSprite(g.hitBoxPositions[random_index], g.consts["window"]["height"]*1.25)
        self.add(sprite)
        self.boxes[random_index].append(sprite)

    def on_key_press (self, k, modifiers):
        if (k in g.keyBindings):
            children = self.boxes[g.keyBindings.index(k)]
            if(children):
                bestOne = min([abs(child.y - g.hitBoxHeight) for child in children])
                self.text.element.text = str(g.keyBindings.index(k)) + " " + str(bestOne)
                bestChild = [child for child in children if abs(child.y - g.hitBoxHeight) == bestOne][0] #yuck
                if(bestChild):
                    if(bestOne < 7.5):
                        children.remove(bestChild)
                        action = (ac.MoveTo((bestChild.x, g.hitBoxHeight)) | ac.FadeOut(0.25) | ac.ScaleBy(1.75, 0.25) ) + ac.CallFuncS(self.remove_child)
                        bestChild.do(action)
                        g.currentSpeed += 2.5
                    elif (bestOne < 12.5):
                        children.remove(bestChild)
                        action = (ac.FadeOut(0.25)) + ac.CallFuncS(self.remove_child)
                        bestChild.do(action)
                        g.currentSpeed += 1

    def remove_child(self, sprite):
        self.remove(sprite)