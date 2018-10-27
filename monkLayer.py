import cocos
import cocos.actions as ac
from cocos.sprite import Sprite

import flowglobals as g

class MonkSprite(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(MonkSprite, self).__init__('assets/monk1.png')
        self.position = x,y
        
class MonkLayer(cocos.layer.Layer):
    def __init__(self, state):
        super(MonkLayer, self).__init__()
        self.s = state
        self.monkSprite = MonkSprite(g.screenWidth/2, g.screenHeight/2)
        self.add(self.monkSprite)
        self.schedule(self.update)
        self.minOpacity = 175

    def update(self, dt):
        if(self.s.currentLevel < g.script_startflying):
            toSubtract = (self.s.currentLevel / g.script_startflying) * (255 -self.minOpacity)
            self.monkSprite.opacity = 255 - toSubtract

    def win(self):
        self.winSprite = cocos.sprite.Sprite('assets/winscreen.PNG', position = (g.screenWidth/2, g.screenHeight/2))
        self.add(self.winSprite)
        action = ac.Delay(4) + ac.FadeOut(3)
        self.winSprite.do(action)