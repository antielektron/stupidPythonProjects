import pygame
from pygame.locals import *
import tools
import gitter

KACHEL_ALPHA_ACTIVE = 1.0
KACHEL_ALPHA_INACTIVE = 0.175
KACHEL_ALPHA_SELECT = 0.5
KACHEL_ALPHA_STEPFACTOR = 0.1


class kachel(object):
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        #alphaverwaltung:
        self.currentAlpha = KACHEL_ALPHA_INACTIVE
        self.alpha = KACHEL_ALPHA_INACTIVE

        self.r = 0.5-0.5/float(gitter.GITTER_W)*float(x)
        self.g = 0.5*float(y)/float(gitter.GITTER_H)
        self.b = float(x)/float(gitter.GITTER_W)

        #verwaltungstechnisches:
        self.isActive = False
        self.isSelect = False

    #nen paar getters und setters:

    def getPos(self):
        return (self.x,self.y,self.w,self.h)

    def isActive(self):
        return self.isActive

    def isSelect(self):
        return self.isSelect

    def activate(self):
        self.isActive = True
        self.alpha = KACHEL_ALPHA_ACTIVE

    def deactivate(self):
        self.isActive = False
        self.alpha = KACHEL_ALPHA_INACTIVE

    def toggle(self):
        self.isActive = not self.isActive
        if self.isActive:
            self.alpha = KACHEL_ALPHA_ACTIVE
        else:
            self.alpha = KACHEL_ALPHA_INACTIVE

    def select(self):
        if not self.isActive:
            self.isSelect = True
            self.alpha = KACHEL_ALPHA_SELECT

    def deselect(self):
        if not self.isActive:
            self.isSelect = False
            self.alpha = KACHEL_ALPHA_INACTIVE

    #update:
    def update(self):
        self.currentAlpha += float(self.alpha - self.currentAlpha)*KACHEL_ALPHA_STEPFACTOR

    def draw(self):
        tools.drawRect((self.x*self.w+2,self.y*self.h+2,self.w-2,self.h-2),0,(self.r,self.g,self.b,self.currentAlpha))


