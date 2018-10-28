import cocos
import cocos.actions as ac
from cocos.sprite import Sprite

import flowglobals as g

class MonkSprite(cocos.sprite.Sprite):
    def __init__(self, x, y, lvl, scale = 1):
        super(MonkSprite, self).__init__('assets/monk' + str(lvl) + '.png', scale = scale)
        self.position = x,y
        
class MonkLayer(cocos.layer.Layer):
    def __init__(self, state):
        super(MonkLayer, self).__init__()
        self.s = state
        self.monkSprite1 = MonkSprite(g.screenWidth/2, g.screenHeight/2, 1)
        self.add(self.monkSprite1)
        self.monkSprite2 = MonkSprite(g.screenWidth/2, g.screenHeight/2, 2, scale = 1.25)
        self.add(self.monkSprite2)

        self.schedule(self.update)
        self.minOpacity = 175

    def update(self, dt):
        if(self.s.currentLevel < g.script_startflying):
            self.monkSprite2.opacity = 0
            toSubtract = (self.s.currentLevel / g.script_startflying) * (255 -self.minOpacity)
            self.monkSprite1.opacity = 255 - toSubtract
        elif(self.s.currentLevel < g.script_4):
            self.monkSprite1.opacity = self.minOpacity
            self.monkSprite2.opacity = 0
        else:
            self.monkSprite2.opacity = self.minOpacity
            self.monkSprite1.opacity = 0


    def win(self):
        self.winSprite = cocos.sprite.Sprite('assets/winscreen.PNG', position = (g.screenWidth/2, g.screenHeight/2))
        self.add(self.winSprite)
        action = ac.Delay(4) + ac.FadeOut(3)
        self.winSprite.do(action)