#!/usr/bin/env python3

import pygame
from OpenGL.GL import *
from pygame.locals import *

import argparse
import sys
import random
import time

#TODO: remove global vars

pygame.init()

window_w = 1600
window_h = 900

livingSpaceWidth = 64
livingSpaceHeight = 36

creatureW = window_w/(livingSpaceWidth)
creatureH = window_h/(livingSpaceHeight)

FPS = 30

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

livingSpace = []
livingSpaceColor = []

update_queue = []
old_update_queue = []

# doubled draw buffer because of display double buffering
draw_buffer = []
draw_buffer_old = []

antPosition = (livingSpaceWidth // 2, livingSpaceHeight // 2)
antRotation = NORTH

num_colors = 2
color_list = []
code = [False,True]

# store number of active cells
num_active_cells = 0

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
    global color_list
    global num_colors
    color_list = []
    for i in range(num_colors):
        color_list.append(HSVtoRGB(i * 360.0 / num_colors,1,1))


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

    # draw langton's ant quad:
    x = antPosition[0] * creatureW
    y = antPosition[1] * creatureH

    offX = creatureW / 2
    offY = creatureH / 2

    glColor4f(1,1,1,0.5)

    glVertex3f(x + offX, y, 0.0) if antRotation != SOUTH else glVertex3f(x + offX, y + creatureH/2, 0.0)
    glVertex3f(x + creatureW - 1, y + offY, 0.0) if antRotation != WEST else glVertex3f(x + creatureW/2, y + offY, 0.0)
    glVertex3f(x + offX, y + creatureH - 1, 0.0) if antRotation != NORTH else glVertex3f(x + offX, y + creatureH/2, 0.0)
    glVertex3f(x, y + offY, 0.0) if antRotation != EAST else glVertex3f(x + creatureW/2, y + offY, 0.0)

    glEnd()

    draw_buffer_old = draw_buffer
    draw_buffer = []


def activate(i,j,key = 1):
    global num_active_cells
    if livingSpace[i][j] == 0:
        num_active_cells += 1

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
    global num_active_cells
    if livingSpace[i][j] != 0:
        num_active_cells -= 1
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

def move_ant(dx, dy):
    global antPosition
    global antRotation

    # finally move:
    antPosition = (antPosition[0] + dx, antPosition[1] + dy)

    # wrap around:
    if antPosition[0] < 0:
        antPosition = (livingSpaceWidth - 1, antPosition[1])
    elif antPosition[0] >= livingSpaceWidth:
        antPosition = (0, antPosition[1])
    if antPosition[1] < 0:
        antPosition = (antPosition[0], livingSpaceHeight - 1)
    elif antPosition[1] >= livingSpaceHeight:
        antPosition = (antPosition[0], 0)

    update_queue.append(antPosition)



def update_ant():
    global antPosition
    global antRotation
    # if we have only two colors, we will switch between on and off
    if num_colors == 2:
        # switch cell
        if isAlive(antPosition[0], antPosition[1]):
            deactivate(antPosition[0], antPosition[1])
        else:
            activate(antPosition[0], antPosition[1])

        # turn
        code_index = 1 if isAlive(antPosition[0], antPosition[1]) else 0

        if code[code_index]:
            # turn right
            antRotation = (antRotation + 3) % 4
        else:
            # turn left
            antRotation = (antRotation + 1) % 4

    else:
        # if we have more than 3 colors, we use the color code
        old_key = livingSpace[antPosition[0]][antPosition[1]] - 1
        new_key = (livingSpace[antPosition[0]][antPosition[1]]) % num_colors + 1  # avoiding key zero, it is deactivated
        if not isAlive(antPosition[0], antPosition[1]):
            # first activation time, increase key:
            new_key += 1
            old_key += 1

        #determine direction:
        if code[old_key]:
            # turn left:
            antRotation = (antRotation + 3) % 4
        else:
            # turn right:
            antRotation = (antRotation + 1) % 4

        # then activate with new key
        activate(antPosition[0], antPosition[1], new_key)


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

    move_ant(dx,dy)


def main():

    global livingSpaceWidth
    global livingSpaceHeight
    global creatureW
    global creatureH
    global antPosition
    global antRotation
    global window_w
    global window_h
    global color_list
    global num_colors
    global code

    # parsing args:
    parser = argparse.ArgumentParser(description="langton\'s ant simulation tool", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--steps', dest='steps', default = 20 , help='steps per second. Default = 20')
    parser.add_argument('--w', dest='w', default = livingSpaceWidth, help = 'field width')
    parser.add_argument('--h', dest='h', default=livingSpaceHeight, help = 'field height')
    parser.add_argument('--calc', dest='calc', default=0, help='calculate steps and only display result')
    parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
    parser.add_argument('--window_w', dest='win_w', default=window_w, help='window width')
    parser.add_argument('--window_h', dest='win_h', default=window_h, help='window height')
    parser.add_argument('--configurator', dest='configurator', action='store_true', help='start in field edit mode')
    parser.add_argument('--code', dest='code', default='10', help='binary code for the ant (\'10\' corresponds to the starndard ant behaviour). 1 means \'turn left\', 0 means \'turn right\'')
    parser.add_argument('--file', dest='file', default='', help='writing number of living cells per step in this file')
    parser.add_argument('--pattern', dest='pattern', default='0',
                        help='initial pattern for the field. Possible values:\n' +
                        '\t * 0: all fields inactive\n' +
                        '\t * 1: all fields active\n' +
                        '\t * check: checkboard pattern\n' +
                        '\t * horizontal: horizontal stripes\n' +
                        '\t * vertical: vertical stripes\n' +
                        '\t * random: random values\n')

    parser.set_defaults(fullscreen=False)
    parser.set_defaults(configurator=False)

    if (len(sys.argv) == 1):

        # no parameters given. Print help and ask user at runtime for options:

        settings = {}
        settings["steps"] = 20
        settings["w"] = livingSpaceWidth
        settings["h"] = livingSpaceHeight
        settings["calc"] = 0
        settings["fullscreen"] = False
        settings["window_w"] = window_w
        settings["window_h"] = window_h
        settings["configurator"] = False
        settings["code"] = '10'
        settings["file"] = ""
        settings["pattern"] = '0'

        while True:
            parser.print_help()
            print("current settings:")
            for key in settings.keys():
                print(str(key) + " = " + str(settings[key]))
            a = input("enter parameter to change. press enter to continue:")
            if len(a) == 0:
                break
            val = input("enter new value:")
            settings[a] = val
        # passing settings to parser:
        parser.set_defaults(steps=settings["steps"])
        parser.set_defaults(w=settings["w"])
        parser.set_defaults(h=settings["h"])
        parser.set_defaults(calc=settings["calc"])
        parser.set_defaults(fullscreen=settings["fullscreen"])
        parser.set_defaults(window_w=settings["window_w"])
        parser.set_defaults(window_h=settings["window_h"])
        parser.set_defaults(configurator=settings["configurator"])
        parser.set_defaults(code=settings["code"])
        if len(settings["file"]) > 0:
            parser.set_defaults(file=settings["file"])
        parser.set_defaults(pattern=settings["pattern"])




    args = parser.parse_args()
    steps_per_sec = int(args.steps)
    livingSpaceWidth = int(args.w)
    livingSpaceHeight = int(args.h)
    calc = int(args.calc)
    filename = args.file
    fileobj = None
    if len(filename) > 0:
        fileobj = open(filename, mode='w')

    video_flags = OPENGL | HWSURFACE | DOUBLEBUF

    # parse code:
    code = []
    for c in args.code:
        if c == '0':
            code.append(False)
        else:
            code.append(True)

    # generate colors:
    num_colors = len(code)
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

    antPosition = (livingSpaceWidth // 2, livingSpaceHeight // 2)


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

    # apply pattern
    if args.pattern == '0':
        # nothing to do
        pass
    elif args.pattern == '1':
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                activate(i,j)
    elif args.pattern == 'check':
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                if (i + j) % 2 == 0:
                    activate(i,j)
    elif args.pattern == 'horizontal':
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                m = j % num_colors
                if num_colors > 2:
                    m += 1
                if m != 0:
                    activate(i,j,m)
    elif args.pattern == 'vertical':
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                m = i % num_colors
                if num_colors > 2:
                    m += 1
                if m != 0:
                    activate(i,j,m)
    elif args.pattern == 'random':
        r = random.Random(time.time())
        for i in range(livingSpaceWidth):
            for j in range(livingSpaceHeight):
                k = r.randint(0,num_colors - 1)
                if num_colors > 2:
                    k += 1
                if k != 0:
                    activate(i,j,k)
    else:
        print("error. unknown pattern")
        parser.print_help()
        sys.exit(-1)

    if (calc > 0):
        for i in range(calc):
            update_ant()

    #main loop:
    while True:


        ticktime = clock.tick(FPS)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        update_field()
        draw()

        field_draws += len(draw_buffer) + len(draw_buffer_old)
        frames += 1

        if frames % FPS == 0:
            print("average field draws per frame: " + str(field_draws/FPS))
            field_draws = 0


        pygame.display.flip()

        if configurator_mode:
            # move with keys:
            if event.type == KEYDOWN:
                draw_buffer.append((antPosition[0],antPosition[1]))
                if event.key == K_DOWN:
                    move_ant(0,+1)
                elif event.key == K_UP:
                    move_ant(0,-1)
                elif event.key == K_LEFT:
                    move_ant(-1,0)
                elif event.key == K_RIGHT:
                    move_ant(+1,0)
                elif event.key == K_SPACE:
                    new_key = (livingSpace[antPosition[0]][antPosition[1]]) % num_colors + 1
                    if not isAlive(antPosition[0], antPosition[1]):
                        new_key += 1
                    activate(antPosition[0], antPosition[1], new_key)
                elif event.key == K_BACKSPACE:
                    deactivate(antPosition[0],antPosition[1])
                elif event.key == K_LCTRL:
                    antRotation = (antRotation - 1) % 4
                    move_ant(0,0)
                elif event.key == K_RCTRL:
                    antRotation = (antRotation + 1) % 4
                    move_ant(0,0)
                elif event.key == K_RETURN:
                    configurator_mode = False

        else:

            if (calc == 0):
                counter += 1

            if logic_frame_pause >= 1:
                if counter > logic_frame_pause:
                    update_ant()
                    if fileobj != None:
                        fileobj.write(str(num_active_cells) + '\n')
                    counter = 0
            else:
                # multiple calculations per frame:
                for i in range(int(1 / logic_frame_pause)):
                    update_ant()
                    if fileobj != None:
                        fileobj.write(str(num_active_cells) + '\n')

            # switch to configurator mode:
            if event.type == KEYDOWN and event.key == K_RETURN:
                configurator_mode = True
    if fileobj != None:
        fileobj.close()


if __name__ == '__main__':
    main()
