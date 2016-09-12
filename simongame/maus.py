import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import eventmanager

BUTTON_PRESSED = 0
BUTTON_HOLD = 1
BUTTON_RELEASED = 2
BUTTON_INACTIVE = 3

class maus(object):
    def __init__(self):
        self.pressed = [False,False,False]
        self.hold = [False,False,False]
        self.release = [False, False, False]
        self.inactive = [True,True,True]

        self.pos = (0,0)
    
    def update(self):
        pressed = pygame.mouse.get_pressed()
        self.pos = pygame.mouse.get_pos()
        for i in range(3):

            if self.pressed[i]:
                self.pressed[i] = False
                self.hold[i] = True

            if self.release[i]:
                self.release[i] = False
                self.inactive[i] = True

            if pressed[i]:
                if self.inactive[i]:
                    self.inactive[i] = False
                    self.pressed[i] = True
            else:
                if self.hold[i]:
                    self.hold[i] = False
                    self.release[i] = True




    def getState(self,button):
        if self.pressed[button]:
            
            return BUTTON_PRESSED
        elif self.release[button]:
            
            return BUTTON_RELEASED

        elif self.hold[button]:
            return BUTTON_HOLD

        return BUTTON_INACTIVE

    def getPos(self):
        return self.pos
    