#!/usr/bin/python

import pygame
import math
from pygame.locals import *
from sys import exit
from ball import *
from bat import *
from eventhandler import *
import eventhandler
pygame.init();

#spielvariablen:

PLAYER_SPEED = 8
KI_SPEED = 12

GAMESPEED = 1.0
MAXSPEED = 3.0
SPEEDFAKTOR = 1.2

PADHEIGHT = 100.0

FPS = 60

#hole infos ueber die derzeitige displaykonfiguration
dinfo = pygame.display.Info();

#mache einen neuen Bildschirm in vollbild
screen = pygame.display.set_mode(( dinfo.current_w, dinfo.current_h),FULLSCREEN | HWSURFACE,dinfo.bitsize);
#screen = pygame.display.set_mode(( 800, 600),HWSURFACE,dinfo.bitsize);

font = pygame.font.SysFont("arial", 30);


myball = ball(1050,50,-5,5)

batleft = bat(20,dinfo.current_h/2-PADHEIGHT/2, 30, PADHEIGHT, PLAYER_SPEED, dinfo.current_h)
batright =  bat(dinfo.current_w-50,dinfo.current_h/2-PADHEIGHT/2, 30, PADHEIGHT, KI_SPEED, dinfo.current_h)

e_handler=EventHandler()
keys = KeyHandler()
keys.registerKey(K_ESCAPE)
keys.registerKey(K_UP)
keys.registerKey(K_DOWN)

clock = pygame.time.Clock()

speed = GAMESPEED;

pointleft = 0
pointright = 0

error_counter = 0

ticktime = 0.0

realFps = 0
fpsCounter = 0

lastFps = 0


while True:
    
    #timer:
    
    ticktime = clock.tick(FPS)
    
    #zeichenoperationen:
    if (ticktime<1000.0/FPS+10):
        screen.fill((0,0,0))
        myball.draw(screen)
        batleft.draw(screen)
        batright.draw(screen)
        screen.blit( font.render(str(""+str(pointleft)+" : "+str(pointright)), True, (255, 255, 255)), (dinfo.current_w/2-30, 20) )
        screen.blit( font.render(str(lastFps), True, (255, 255, 255)), (dinfo.current_w/2-30, 60) )

        pygame.display.update()
        
        realFps +=1
    
    #logik:
    
    e_handler.update()
    keys.update(e_handler)
    fpsCounter +=1
    
    if fpsCounter >= FPS:
        lastFps = realFps
        fpsCounter = 0
        realFps = 0
    
    #spieler:
    if keys.getKeyState(K_UP) == KEY_HOLD:
        batleft.moveUp()
    if keys.getKeyState(K_DOWN) == KEY_HOLD:
        batleft.moveDown()
    
    #computer:
    if myball.getY() < batright.getY()+20:
        batright.moveUp()
    if myball.getY() > batright.getY()+PADHEIGHT-20:
        batright.moveDown()
    
    #kollisionsabfragen:
    
    if batleft.checkCollision(myball.getX(), myball.getY()) and myball.getDx() <0:
        x = myball.getX()
        y = myball.getY()
        
        y2 = batleft.getY()
        
        dy = (float(y-y2)/PADHEIGHT*10.0)-5.0
        dx = 7.5-math.fabs(dy)
        
        myball.setDx(dx*speed)
        myball.setDy(dy*speed)
        
        speed *= SPEEDFAKTOR
    
    if batright.checkCollision(myball.getX(), myball.getY()) and myball.getDx()>0:
        x = myball.getX()
        y = myball.getY()
        
        y2 = batright.getY()
        
        dy = (float(y-y2)/PADHEIGHT*10.0)-5.0
        dx = 7.5-math.fabs(dy)
        
        myball.setDx(-dx*speed)
        myball.setDy(dy*speed)
        
        speed *= SPEEDFAKTOR
    
    if speed > MAXSPEED:
        speed = MAXSPEED
    
    if myball.getY()-10<0 or myball.getY()+10>dinfo.current_h:
        myball.setDy(-myball.getDy())
    myball.update()
    
    
    
    if myball.getX() < 0:
        pointright +=1
        speed = GAMESPEED
        myball.setX(dinfo.current_w/2)
        myball.setY(dinfo.current_h/2)
        myball.setDx(-6)
        myball.setDy(0)
        
    if myball.getX() > dinfo.current_w:
        pointleft +=1
        speed = GAMESPEED
        myball.setX(dinfo.current_w/2)
        myball.setY(dinfo.current_h/2)
        myball.setDx(6)
        myball.setDy(0)
    
    if keys.getKeyState(K_ESCAPE) != KEY_INACTIVE:
        exit()
        

