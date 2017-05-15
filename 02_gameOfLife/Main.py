#!/usr/bin/python
import pygame
import random
from OpenGL.GL import *
from pygame.locals import *

import argparse

#TODO: remove global vars

pygame.init()

window_w = 1600
window_h = 900

livingSpaceWidth = 64
livingSpaceHeight = 36

creatureW = window_w/(livingSpaceWidth)
creatureH = window_h/(livingSpaceHeight)

FPS = 30

livingSpace = []

draw_buffer = []
draw_buffer_old = []


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
    global draw_buffer
    global draw_buffer_old
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0,0.0,3.0)


    glBegin(GL_QUADS)
    for column, row in draw_buffer + draw_buffer_old:
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

    draw_buffer_old = draw_buffer
    draw_buffer = []

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
                    draw_buffer.append((column, row))
                if not isAlive(column,row):
                    livingSpace[column][row] = float(livingSpace[column][row])/1.2
                    draw_buffer.append((column, row))

            else:
                livingSpace[column][row] = float(livingSpace[column][row])/1.2
                draw_buffer.append((column, row))

            if livingSpace[column][row] < 20:
                livingSpace[column][row] = 0

def main():
    global livingSpaceWidth
    global livingSpaceHeight
    global creatureW
    global creatureH
    global window_w
    global window_h

    # parsing args:
    parser = argparse.ArgumentParser(description="game of life")
    parser.add_argument('--steps', dest='steps', default = 20 , help='steps per second')
    parser.add_argument('--w', dest='w', default = livingSpaceWidth, help = 'field width')
    parser.add_argument('--h', dest='h', default=livingSpaceHeight, help = 'field height')
    #parser.add_argument('--calc', dest='calc', default=0, help='calculate steps and only display result')
    #parser.add_argument('--default', dest='default', default=0, help='setting all fields to this value')
    parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
    parser.add_argument('--window_w', dest='win_w', default=window_w, help='window width')
    parser.add_argument('--window_h', dest='win_h', default=window_h, help='window height')
    parser.add_argument('--configurator', dest='configurator', action='store_true', help='start in field edit mode')
    #parser.add_argument('--code', dest='code', default='01', help='binary code for the ant (\'01\' corresponds to the starndard ant behaviour)')

    parser.set_defaults(fullscreen=False)
    parser.set_defaults(configurator=False)

    args = parser.parse_args()
    steps_per_sec = int(args.steps)
    livingSpaceWidth = int(args.w)
    livingSpaceHeight = int(args.h)

    video_flags = OPENGL | HWSURFACE | DOUBLEBUF


    if args.fullscreen:
        video_flags = OPENGL | HWSURFACE | DOUBLEBUF | FULLSCREEN
        dinfo = pygame.display.Info()
        window_w = dinfo.current_w
        window_h = dinfo.current_h
    else:
        window_w = int(args.win_w)
        window_h = int(args.win_h)


    creatureW = window_w / (livingSpaceWidth)
    creatureH = window_h / (livingSpaceHeight)

    #antPosition = (livingSpaceWidth // 2, livingSpaceHeight // 2)


    pygame.display.set_mode((window_w,window_h),video_flags)

    initLivingSpace()

    resize((window_w, window_h))
    init()

    clock = pygame.time.Clock()

    frames = 0
    counter = 0
    logic_frame_pause = FPS / steps_per_sec
    configurator_mode = bool(args.configurator)

    field_draws = 0


    #Hauptschleife:
    while True:


        ticktime = clock.tick(FPS)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        draw()

        field_draws += len(draw_buffer) + len(draw_buffer_old)
        frames += 1

        if frames % FPS == 0:
            print("average field draws per frame: " + str(field_draws / FPS))
            field_draws = 0

        pygame.display.flip()

        if configurator_mode:
            # move with keys:
            if event.type == KEYDOWN:
            #    draw_buffer.append((antPosition[0],antPosition[1]))
            #    if event.key == K_DOWN:
            #        move_ant(0,+1)
            #    elif event.key == K_UP:
            #        move_ant(0,-1)
            #    elif event.key == K_LEFT:
            #        move_ant(-1,0)
            #    elif event.key == K_RIGHT:
            #        move_ant(+1,0)
            #    elif event.key == K_SPACE:
            #        new_key = (livingSpace[antPosition[0]][antPosition[1]]) % num_colors + 1
            #        if not isAlive(antPosition[0], antPosition[1]):
            #            new_key += 1
            #        activate(antPosition[0], antPosition[1], new_key)
            #    elif event.key == K_BACKSPACE:
            #        deactivate(antPosition[0],antPosition[1])
                if event.key == K_RETURN:
                    configurator_mode = False

        counter += 1

        if logic_frame_pause >= 1:
            if counter > logic_frame_pause:
                calculateNextGeneration()
                counter = 0
        else:
            # multiple calculations per frame:
            for i in range(int(1 / logic_frame_pause)):
                calculateNextGeneration()

        # switch to configurator mode:
        if event.type == KEYDOWN and event.key == K_RETURN:
            configurator_mode = True



if __name__ == '__main__':
    main()
