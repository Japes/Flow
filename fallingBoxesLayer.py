#other stuff
import random
import time

#cocos stuff
import cocos
import cocos.actions as ac
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.audio.pygame.mixer import Sound

#my stuff
import flowglobals as g

spriteScale = 0.75

class FallingBoxSprite(cocos.sprite.Sprite):
    def __init__(self, x, y, state):
        super(FallingBoxSprite, self).__init__('assets/circle.png', scale = spriteScale)
        self.position = x,y
        action = ac.MoveTo((self.position[0], -g.consts["window"]["height"]*1.25), 8)
        self.do(action)
        self.schedule_interval(self.checkForDeath, 0.25)
        self.haveAppliedPenalty = False
        self.s = state

    def checkForDeath(self, dt):
        if(self.y < (g.hitBoxHeight - self.height/2) and (not self.haveAppliedPenalty)):
            if(self.s.currentSpeed > 5):
                self.s.currentSpeed /= 2
            else:
                self.s.currentSpeed -= 7.5
            self.haveAppliedPenalty = True

        if(self.y < -self.height):
            self.kill()


class FallingBoxesLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, state):
        super(FallingBoxesLayer, self).__init__()
        self.s = state
        self.__bps_granularity = 8.0 #beats per second
        self.boxes = []
        for range in g.keyBindings:
            self.boxes.append([])
        self.__barCounter = 0 #which "beat" of the current musical "bar" are we on

        self.sounds = []
        for s in g.hitboxSounds:
            self.sounds.append(Sound(s))
        self.missSounds = []
        for s in g.hitboxMissSounds:
            self.missSounds.append(Sound(s))
        
        ###"public api" stuff...
        self.maxBPS = 1
        self.ratioSkips = 0.0
        self.ratioInbetweeners = 0
        ###

        self.schedule_interval(self.generateBox, 1/self.__bps_granularity)

    #called by scheduler
    def generateBox(self, dt):
        interval = self.__bps_granularity / self.maxBPS #time between beats
        halfInterval = interval/2
        isABeat = self.__barCounter % interval == 0
        isAHalfBeat = self.__barCounter % halfInterval == 0
        if(isABeat or (random.random() < self.ratioInbetweeners and isAHalfBeat)):
            if(random.random() > self.ratioSkips):
                random_index = random.randrange(len(g.keyBindings))
                sprite = FallingBoxSprite(g.hitBoxPositions[random_index], g.consts["window"]["height"]*1.25, self.s)
                self.add(sprite)
                self.boxes[random_index].append(sprite)

        self.__barCounter += 1
        if(self.__barCounter >= self.__bps_granularity):
            self.__barCounter = 0

    def on_key_press (self, k, modifiers):
        if (k in g.keyBindings):
            self.s.timeLastKeyPress = time.time()
            children = self.boxes[g.keyBindings.index(k)]
            if(children):
                bestOne = min([abs(child.y - g.hitBoxHeight) for child in children])
                bestChild = [child for child in children if abs(child.y - g.hitBoxHeight) == bestOne][0] #yuck
                if(bestChild):
                    if(bestOne < 8.5):
                        children.remove(bestChild)
                        action = (ac.MoveTo((bestChild.x, g.hitBoxHeight)) | ac.FadeOut(0.25) | ac.ScaleBy(1.75, 0.25) ) + ac.CallFuncS(self.remove_child)
                        bestChild.do(action)
                        self.s.currentSpeed += 2.5
                        self.sounds[g.keyBindings.index(k)].play() # Play right now
                    elif (bestOne < 20):
                        children.remove(bestChild)
                        action = (ac.FadeOut(0.25)) + ac.CallFuncS(self.remove_child)
                        bestChild.do(action)
                        self.s.currentSpeed += 1
                        self.missSounds[g.keyBindings.index(k)].play() # Play right now
                    else:
                        #apply penalty! (to stop spamming)
                        self.s.currentSpeed -= 5

    def remove_child(self, sprite):
        self.remove(sprite)