import tools
import eventmanager
import maus

BUTTON_ALPHA_INACTIVE = 0.3
BUTTON_ALPHA_SELECT = 0.8
BUTTON_ALPHA_CLICKED = 1.0

class button(object):

    def __init__(self, mouse, posRect, color, text, font):
        self.posRect = posRect
        self.color = color

        self.alpha = BUTTON_ALPHA_INACTIVE

        self.text = text
        self.font = font

        self.mouse = mouse

        self.clicked = False

    def isClicked(self):

        return self.mouse.getState(0) == maus.BUTTON_RELEASED and tools.is2DPointCollision(self.mouse.getPos(),self.posRect)

    def update(self):
        if tools.is2DPointCollision(self.mouse.getPos(),self.posRect):
            if self.mouse.getState(0) == maus.BUTTON_HOLD:
                self.alpha = BUTTON_ALPHA_CLICKED
            else:
                self.alpha = BUTTON_ALPHA_SELECT
        else:
            self.alpha = BUTTON_ALPHA_INACTIVE

    def draw(self):
        tools.drawRect((self.posRect[0]-2,self.posRect[1]-2,self.posRect[2]+4,self.posRect[3]+4),0,(0.0,0.0,0.0,1.0))
        tools.drawRect(self.posRect,0,(self.color[0],self.color[1],self.color[2],self.alpha))
        tools.writePerFTGL(self.text,self.font,
            (self.posRect[0] + 20,self.posRect[1]+self.posRect[3]/2+8),(1.0,1.0,1.0,1.0))


