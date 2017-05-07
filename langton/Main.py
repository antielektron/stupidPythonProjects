#!/usr/bin/env python3
import pygame
import random
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

import argparse

video_flags = OPENGL | HWSURFACE | DOUBLEBUF

pygame.init()

dinfo = pygame.display.Info();

window_w = 1600
window_h = 900

livingSpaceWidth = 64
livingSpaceHeight = 36

creatureW = window_w/(livingSpaceWidth)
creatureH = window_h/(livingSpaceHeight)

FPS = 60

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

livingSpace = []

update_queue = []
old_update_queue = []

draw_buffer = []
draw_buffer_old = []

antPosition = (livingSpaceWidth // 2, livingSpaceHeight // 2)
antRotation = NORTH

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
            livingSpace[x].append(100)
            draw_buffer.append((x,y))

def isAlive(x,y):
    return livingSpace[x][y] > 101 # epsilon = 1

def draw():
    global draw_buffer
    global draw_buffer_old
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0,0.0,3.0)


    glBegin(GL_QUADS)

    for column,row in draw_buffer + draw_buffer_old:
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

    # draw langton's ant quad:
    x = antPosition[0] * creatureW
    y = antPosition[1] * creatureH

    offX = creatureW / 2
    offY = creatureH / 2

    glColor4f(1,1,1,0.5)

    glVertex3f(x + offX, y, 0.0)
    glVertex3f(x + creatureW - 1, y + offY, 0.0)
    glVertex3f(x + offX, y + creatureH - 1, 0.0)
    glVertex3f(x, y + offX - 1, 0.0)

    glEnd()

    draw_buffer_old = draw_buffer
    draw_buffer = []


def activate(i,j):
    livingSpace[i][j] = 1000
    update_queue.append((i,j))

def deactivate(i,j):
    livingSpace[i][j] = 100
    update_queue.append((i,j))

def update_field():
    global old_update_queue
    global update_queue

    old_update_queue = update_queue
    update_queue = []
    for i,j in old_update_queue:
        draw_buffer.append((i,j))
        if livingSpace[i][j] > 600:
            livingSpace[i][j] = float(livingSpace[i][j]) * 0.98
            if livingSpace[i][j] < 600:
                livingSpace[i][j] = 600
            update_queue.append((i,j))

def move_ant():
    global antPosition
    global antRotation

    # switch cell
    if isAlive(antPosition[0], antPosition[1]):
        deactivate(antPosition[0], antPosition[1])
    else:
        activate(antPosition[0], antPosition[1])

    # turn
    if isAlive(antPosition[0], antPosition[1]):
        # turn right
        antRotation = (antRotation + 1) % 4
    else:
        # turn left
        antRotation = (antRotation + 3) % 4

    # move on step:
    dx = 0
    dy = 0
    if antRotation == NORTH:
        dy = -1
    elif antRotation == SOUTH:
        dy = +1
    elif antRotation == EAST:
        dx = +1
    elif antRotation == WEST:
        dx = -1

    # check bounds:
    if antPosition[0] == 0 and dx < 0:
        dx = 0
    if antPosition[0] == livingSpaceWidth - 1 and dx > 0:
        dx = 0
    if antPosition[1] == 0 and dy < 0:
        dy = 0
    if antPosition[1] == livingSpaceHeight - 1 and dy > 0:
        dy = 0

    # finally move:
    antPosition = (antPosition[0] + dx, antPosition[1] + dy)
    update_queue.append(antPosition)



def update_ant():
    global antPosition
    global antRotation

    move_ant()


def main():

    global livingSpaceWidth
    global livingSpaceHeight
    global creatureW
    global creatureH
    global antPosition

    # parsing args:
    parser = argparse.ArgumentParser(description="langton's ant")
    parser.add_argument('--steps', dest='steps', default = 20 , help='steps per second')
    parser.add_argument('--w', dest='w', default = livingSpaceWidth, help = 'field width')
    parser.add_argument('--h', dest='h', default=livingSpaceHeight, help = 'field height')
    parser.add_argument('--calc', dest='calc', default=0, help='calculate steps and only display result')
    parser.add_argument('--default', dest='default', default=0, help='setting all fields to this value')

    args = parser.parse_args()
    steps_per_sec = int(args.steps)
    livingSpaceWidth = int(args.w)
    livingSpaceHeight = int(args.h)
    calc = int(args.calc)



    creatureW = window_w / (livingSpaceWidth)
    creatureH = window_h / (livingSpaceHeight)

    antPosition = (livingSpaceWidth // 2, livingSpaceHeight // 2)


    pygame.display.set_mode((window_w,window_h),video_flags)

    initLivingSpace()

    if int(args.default) != 0:
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                activate(i,j)

    resize((window_w, window_h))
    init()

    clock = pygame.time.Clock()

    frames = 0
    counter = 0
    logic_frame_pause = FPS / steps_per_sec

    if (calc > 0):
        for i in range(calc):
            update_ant();

    #main loop:
    while True:


        ticktime = clock.tick(FPS)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        update_field();
        draw()

        pygame.display.flip()

        if (calc == 0):
            counter += 1

        if counter > logic_frame_pause:
            update_ant()
            counter = 0



if __name__ == '__main__':
    main()
