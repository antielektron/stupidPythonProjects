#!/usr/bin/env python3
import pygame
from OpenGL.GL import *
from pygame.locals import *
from cellular import *

import argparse

#TODO: remove global vars

# NOTE: modified python script from a multi color langton's ant implementation, so
# maybe some variable names are a little bit confusing...

pygame.init()

window_w = 1600
window_h = 900

livingSpaceWidth = 84
livingSpaceHeight = 47

creatureW = window_w/(livingSpaceWidth)
creatureH = window_h/(livingSpaceHeight)

FPS = 30

livingSpace = []
livingSpaceColor = []

update_queue = []
old_update_queue = []

# doubled draw buffer because of display double buffering
draw_buffer = []
draw_buffer_old = []

current_iteration = 0

num_colors = 2
color_list = []
code = 0
r = 1

# helper function for colors:
def HSVtoRGB(h,s,v):
    c = v*s
    x = c*(1-abs((h/60)% 2 -1))
    m = v-c
    rr=0
    gg=0
    bb=0
    if(h<60):
        rr=c
        gg=x
        bb=0
    elif (h < 120):
        rr = x
        gg = c
        bb = 0
    elif (h < 180):
        rr = 0
        gg = c
        bb = x
    elif (h < 240):
        rr=0
        gg=x
        bb=c
    elif (h < 300):
        rr = x
        gg = 0
        bb = c
    elif (h < 360):
        rr = c
        gg = 0
        bb = x

    return(rr+m,gg+m,bb+m)

def generate_colors():
    """
    generate colors linear over HSV Space (one color for every possible state, not yet supported, but maybe in the future)
    :return: 
    """
    global color_list
    global num_colors
    color_list = []
    for i in range(num_colors):
        color_list.append(HSVtoRGB(i * 360.0 / num_colors,1,1))


def resize(shape):
    """
    Init opengl viewport
    :param shape: 
    :return: 
    """
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
        livingSpaceColor.append([])
        for y in range(livingSpaceHeight):
            livingSpace[x].append(0)
            rgba = [float(x)/float(livingSpaceWidth), float(livingSpaceWidth-x)/float(livingSpaceWidth), float(y)/float(livingSpaceHeight),0.15]
            livingSpaceColor[x].append(rgba)
            draw_buffer.append((x,y))

def isAlive(x,y):
    return livingSpace[x][y] != 0

def draw():
    global draw_buffer
    global draw_buffer_old
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0,0.0,3.0)


    glBegin(GL_QUADS)

    for column,row in draw_buffer + draw_buffer_old:
        r,g,b,a = livingSpaceColor[column][row]

        #glColor4f(255, 0, 0, 1.0)
        glColor4f(a * r, a * g, a * b, 1.0)
        x = column * creatureW
        y = row * creatureH

        glVertex3f(x,y,0.0)
        glVertex3f(x + creatureW-1.0,y,0.0)
        glVertex3f(x+creatureW-1,y+creatureH-1,0.0)
        glVertex3f(x,y+creatureH-1,0.0)


    draw_buffer_old = draw_buffer
    draw_buffer = []


def activate(i,j,key = 1):
    """
    activate field (i,j)
    :param i: 
    :param j: 
    :param key: 
    :return: 
    """
    livingSpace[i][j] = key
    if num_colors > 2:
        livingSpaceColor[i][j] = [
            color_list[key - 1][0],
            color_list[key - 1][1],
            color_list[key - 1][2],
            1.0
        ]
    else:
        livingSpaceColor[i][j][3] = 1.0
    update_queue.append((i,j))

def deactivate(i,j):
    """
    deactivate field (i,j)
    :param i: 
    :param j: 
    :return: 
    """
    livingSpace[i][j] = 0
    # correct color:
    livingSpaceColor[i][j] = [
        float(i) / float(livingSpaceWidth),
        float(livingSpaceWidth - i) / float(livingSpaceWidth),
        float(j) / float(livingSpaceHeight),
        0.6
    ]

    update_queue.append((i,j))

def update_field():
    global old_update_queue
    global update_queue

    old_update_queue = update_queue
    update_queue = []
    for i,j in old_update_queue:
        draw_buffer.append((i,j))
        if livingSpace[i][j] <= 0 and livingSpaceColor[i][j][3] > 0.15:
            livingSpaceColor[i][j][3] *= 0.98
            if livingSpaceColor[i][j][3] < 0.15:
                livingSpaceColor[i][j][3] = 0.15
            update_queue.append((i,j))
        elif livingSpace[i][j] > 0 and livingSpaceColor[i][j][3] > 0.6:
            livingSpaceColor[i][j][3] *= 0.98
            if livingSpaceColor[i][j][3] < 0.6:
                livingSpaceColor[i][j][3] = 0.6
            update_queue.append((i,j))

def updateAutomaton(cells):
    global livingSpaceWidth
    global current_iteration

    for i in range(livingSpaceWidth):
        if cells[i] != 0:
            activate(i, current_iteration)

def main():

    global livingSpaceWidth
    global livingSpaceHeight
    global creatureW
    global creatureH
    global window_w
    global window_h
    global color_list
    global num_colors
    global code
    global current_iteration
    global r

    # parsing args:
    parser = argparse.ArgumentParser(description="one dimensional cellular automaton for k=2 with opengl output")
    parser.add_argument('--steps', dest='steps', default = 60 , help='steps per second')
    parser.add_argument('--w', dest='w', default = livingSpaceWidth, help = 'field width')
    parser.add_argument('--h', dest='h', default=livingSpaceHeight, help = 'field height')
    parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
    parser.add_argument('--window_w', dest='win_w', default=window_w, help='window width')
    parser.add_argument('--window_h', dest='win_h', default=window_h, help='window height')
    parser.add_argument('--code', dest='code', default='150', help='code for the automaton')
    parser.add_argument('--random', dest='random', action='store_true')
    parser.add_argument('--r', dest='r', default=r, help='radius. can be 1 or 2')

    parser.set_defaults(fullscreen=False)
    parser.set_defaults(random=False)
    #parser.set_defaults(configurator=False)

    args = parser.parse_args()
    steps_per_sec = int(args.steps)
    livingSpaceWidth = int(args.w)
    livingSpaceHeight = int(args.h)

    video_flags = OPENGL | HWSURFACE | DOUBLEBUF

    r = int(args.r)
    c = int(args.code)
    startcondition = ""

    if args.random:
        startcondition = "r"
    else:
        startcondition = "s"

    functionTable = code2FunctionTable(c, r)
    cells = generatestart(startcondition, r, livingSpaceWidth)

    # generate colors:
    num_colors = 2 # k is fix for now
    generate_colors()


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

    pygame.display.set_mode((window_w,window_h),video_flags)

    initLivingSpace()

    updateAutomaton(cells)

    resize((window_w, window_h))
    init()

    clock = pygame.time.Clock()

    frames = 0
    counter = 0
    logic_frame_pause = FPS / float(steps_per_sec)

    field_draws = 0

    #main loop:
    while True:


        ticktime = clock.tick(FPS)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        update_field();
        draw()

        field_draws += len(draw_buffer) + len(draw_buffer_old)
        frames += 1

        if frames % FPS == 0:
            print("average field draws per frame: " + str(field_draws/FPS))
            field_draws = 0


        pygame.display.flip()

        counter += 1

        if current_iteration < livingSpaceHeight-1:
            if counter > logic_frame_pause:
                cells = calculateNextStep(functionTable, livingSpaceWidth, cells, r)
                current_iteration += 1
                updateAutomaton(cells)
                print(current_iteration)
                counter = 0




if __name__ == '__main__':
    main()
