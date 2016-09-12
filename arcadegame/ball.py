import pygame
from pygame.locals import *
from sys import exit

class ball(object):
    def __init__(self, x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    
    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y
    
    def setDx(self,dx):
        self.dx = dx
    
    def setDy(self,dy):
        self.dy=dy
        
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getDx(self):
        return self.dx
    
    def getDy(self):
        return self.dy
        
    
    def update(self):
        self.x +=self.dx
        self.y +=self.dy
        
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),Rect(self.x-5,self.y-5,10,10))
    
    