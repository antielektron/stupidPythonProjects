#!/usr/bin/python
import pygame
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

video_flags = OPENGL | HWSURFACE | DOUBLEBUF | FULLSCREEN

pygame.init()

dinfo = pygame.display.Info();

livingSpaceWidth = 48
livingSpaceHeight = 27

creatureW = dinfo.current_w/(livingSpaceWidth)
creatureH = dinfo.current_h/(livingSpaceHeight)

FPS = 40

livingSpace = []

def resize(shape):
    width, height = shape
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, livingSpaceWidth * creatureW, livingSpaceHeight * creatureH, 0.0, -6.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)

def initLivingSpace():
    for x in range(livingSpaceWidth):
        livingSpace.append([])
        for y in range(livingSpaceHeight):
            if random.randint(0,1) ==1:
                livingSpace[x].append(1000)
            else:
                livingSpace[x].append(0)

def isAlive(x,y):
    return livingSpace[x][y] == 1000

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0,0.0,3.0)


    glBegin(GL_QUADS)
    for column in range(livingSpaceWidth):
        for row in range(livingSpaceHeight):
            if livingSpace[column][row] != 0:
                health = float(float(livingSpace[column][row])/1000.0)

                glColor4f(health*(float(column)/float(livingSpaceWidth)),
                    health*(float(livingSpaceWidth-column)/float(livingSpaceWidth)),
                    health*(float(row)/float(livingSpaceHeight)),1.0)
                x = column * creatureW
                y = row * creatureH

                glVertex3f(x,y,0.0)
                glVertex3f(x + creatureW-1.0,y,0.0)
                glVertex3f(x+creatureW-1,y+creatureH-1,0.0)
                glVertex3f(x,y+creatureH-1,0.0)

    glEnd()

def getNeighborCount(x,y):
    count = 0

    xpn = (x + 1) % livingSpaceWidth
    ypn = (y + 1) % livingSpaceHeight
    # nach unten hin ist keine ausnahmebehandlung noetig,
    # da python bei negativen indizes automatisch die liste von hinten
    # durchlaeuft

    # Vorsicht: boolscher Wert wird hier als Int genutzt!
    count += isAlive(x,ypn)
    count += isAlive(xpn,ypn)
    count += isAlive(xpn,y)
    count += isAlive(xpn,y-1)
    count += isAlive(x,y-1)
    count += isAlive(x-1,y-1)
    count += isAlive(x-1,y)
    count += isAlive(x-1,ypn)

    return count

def calculateNextGeneration():
    neighborCount = []
    for column in range(livingSpaceWidth):
        neighborCount.append([])
        for row in range(livingSpaceHeight):
            neighborCount[column].append(getNeighborCount(column,row))

    for column in range(livingSpaceWidth):
        for row in range(livingSpaceHeight):
            if 2 <= neighborCount[column][row] <= 3:
                if neighborCount[column][row] == 3:
                    livingSpace[column][row] = 1000
                if not isAlive(column,row):
                    livingSpace[column][row] = float(livingSpace[column][row])/1.2

            else:
                livingSpace[column][row] = float(livingSpace[column][row])/1.2

            if livingSpace[column][row] < 20:
                livingSpace[column][row] = 0

def main():

    pygame.display.set_mode((dinfo.current_w,dinfo.current_h),video_flags)

    initLivingSpace()
    resize((dinfo.current_w,dinfo.current_h))
    init()

    clock = pygame.time.Clock()

    frames = 0

    #Hauptschleife:
    while True:


        ticktime = clock.tick(FPS)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break


        draw()

        pygame.display.flip()
        calculateNextGeneration()



if __name__ == '__main__':
    main()
