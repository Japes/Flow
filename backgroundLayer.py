#other stuff

#cocos stuff
import cocos
from cocos.sprite import Sprite
import cocos.actions as ac

#my stuff
import flowglobals as g

updateInterval = 0.2

class Sprite1(cocos.sprite.Sprite):
    def __init__(self):
        super(Sprite1, self).__init__('assets/background.jpg', scale=2)
        self.position = g.screenWidth/2,g.screenHeight/2

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.sprite = Sprite1()
        self.add(self.sprite)
        self.schedule_interval(self.updateSpeed, updateInterval)

    #called by scheduler
    def updateSpeed(self, dt):
        move = ac.MoveBy((0, -g.currentSpeed), duration=updateInterval)
        self.sprite.do(move)