import pygame
from pygame.locals import *
from sys import exit

class bat(object):
    
    def __init__(self, x,y,w,h,dy, maxY):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = dy
        self.maxY = maxY
    
    def moveUp(self):
        self.y-= self.dy
        if self.y<0:
            self.y=0
            
    def moveDown(self):
        self.y += self.dy
        if self.y+self.h > self.maxY:
            self.y = self.maxY - self.h
    
    def getY(self):
        return self.y
    
    def checkCollision(self,x,y):
        if x<self.x or x>self.x+self.w:
            return False
        
        if y<self.y or y > self.y + self.h:
            return False
        return True
    
    def draw(self, screen):
        pygame.draw.rect(screen,(255,255,255),Rect(self.x,self.y,self.w,self.h))
    