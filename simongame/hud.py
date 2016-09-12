import pygame
from pygame.locals import *
import tools
from button import *

#hud-Modes:
HUD_MODE_MAINMENU = 0
HUD_MODE_PLAY = 1
HUD_MODE_GAMEOVER = 2

#bissl wat zur GUI:
SIDE_SPACING = 30
BUTTON_HEIGTH = 50
COLOR_FADE_FACTOR = 0.1

class hud(object):
    def __init__(self,posRect,mouse,font):
        self.posRect = posRect
        self.mode = HUD_MODE_MAINMENU
        self.font = font

        #Die Buttons:
        playRect = (posRect[0]+SIDE_SPACING,posRect[1]+posRect[3]/5,posRect[2]-2*SIDE_SPACING,BUTTON_HEIGTH)
        self.play = button(mouse,playRect,(0.0,1.0,0.0),"Los gehts!",font)
        exitRect = (posRect[0]+SIDE_SPACING,posRect[1]+posRect[3]/5+2*BUTTON_HEIGTH,posRect[2]-2*SIDE_SPACING,BUTTON_HEIGTH)
        self.exit = button(mouse,exitRect,(1.0,0.0,0.0),"Tschau mit V!",font)

        okRect = (posRect[0]+SIDE_SPACING,posRect[3]/2+100,posRect[2]-2*SIDE_SPACING,BUTTON_HEIGTH)
        self.ok = button(mouse,okRect,(0.0,1.0,0.0),"okay dokay",font)

        self.bgColor = (0.0,0.0,0.0,1.0)
        self.currentBgColor = self.bgColor

        self.exitClicked = False
        self.playClicked = False
        self.okClicked = False

        self.menuText = "B-)"
        self.messageText = ";-P"

    def getMode(self):
        return self.mode

    def setMode(self,mode):
        self.mode = mode

    def setBgColor(self,color):
        self.bgColor = color

    def setMessage(self,msg):
        self.messageText = msg

    def buttonUpdate(self):
        
        if self.exit.isClicked() == True:
            self.exitClicked = True
            

        if self.play.isClicked() == True:
            self.playClicked = True

        if self.ok.isClicked() == True:
            self.okClicked = True

        self.play.update()
        self.exit.update()
        self.ok.update()

    def isExitClicked(self):
        if self.exitClicked:
            self.exitClicked = False
            return True

        return False

    def isPlayClicked(self):
        if self.playClicked:
            self.playClicked = False
            return True

        return False

    def isOkClicked(self):
        if self.okClicked:
            self.okClicked = False
            return True

        return False

    def update(self):
        if self.mode == HUD_MODE_MAINMENU:
            self.play.update()
            self.exit.update()
        elif self.mode == HUD_MODE_GAMEOVER:
            self.ok.update()

        self.buttonUpdate()

        #hintergrundfarbe blenden:
        r = (self.bgColor[0] - self.currentBgColor[0])*COLOR_FADE_FACTOR
        g = (self.bgColor[1] - self.currentBgColor[1])*COLOR_FADE_FACTOR
        b = (self.bgColor[2] - self.currentBgColor[2])*COLOR_FADE_FACTOR
        a = (self.bgColor[3] - self.currentBgColor[3])*COLOR_FADE_FACTOR

        self.currentBgColor = (self.currentBgColor[0]+ r,
            self.currentBgColor[1]+ g,
            self.currentBgColor[2]+ b,
            self.currentBgColor[3]+ a)



    def draw(self):
        tools.drawRect(self.posRect,0,self.currentBgColor)
        if self.mode == HUD_MODE_MAINMENU:
            self.play.draw()
            self.exit.draw()


        if self.mode == HUD_MODE_GAMEOVER:
            #message
            tools.writePerFTGL("GAME OVER!",self.font,
                (self.posRect[0]+SIDE_SPACING+10,self.posRect[3]/2-30),
                (1.0,0.0,0.0,1.0))
            tools.writePerFTGL(self.messageText,self.font,
                (self.posRect[0]+SIDE_SPACING+10,self.posRect[3]/2+14),
                (1.0,1.0,1.0,1.0))
            self.ok.draw()

        if self.mode == HUD_MODE_PLAY:
            tools.writePerFTGL(self.messageText,self.font,
                (self.posRect[0]+SIDE_SPACING+10,self.posRect[3]/2+14),
                (1.0,1.0,1.0,1.0))

