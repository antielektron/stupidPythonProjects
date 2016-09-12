#!/usr/bin/python3
import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import tools
import gitter
import maus
import hud
import eventmanager

STARTLEVEL = 1

if __name__ == "__main__":

    font = tools.loadFont("GenBasR.ttf",(24,72))

    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=128)

    #sounds laden:

    klick = pygame.mixer.Sound("klick.wav")
    gong = pygame.mixer.Sound("gong.wav")
    error = pygame.mixer.Sound("error.wav")

    dinfo = pygame.display.Info()
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF | FULLSCREEN

    #ein paar variablen zu den seitenverhaeltnissen:
    SCREEN_RATIO = float(dinfo.current_w)/float(dinfo.current_h)  #16:9
    GITTER_RATIO = float(gitter.GITTER_W)/float(gitter.GITTER_H)

    FIELD_W_RATIO = (GITTER_RATIO*float(dinfo.current_h))/float(dinfo.current_w)

    pygame.display.set_mode((dinfo.current_w,dinfo.current_h),video_flags)
    tools.resize((dinfo.current_w,dinfo.current_h))
    tools.GlInit()
    tools.clearScreen()

    eManager = eventmanager.eventmanager()

    mausimaus = maus.maus()

    git = gitter.gitter((dinfo.current_w*FIELD_W_RATIO,dinfo.current_h),eManager,mausimaus,(klick,gong,error))

    sidebar = hud.hud((dinfo.current_w*FIELD_W_RATIO+2,2,dinfo.current_w-dinfo.current_w*FIELD_W_RATIO-4,dinfo.current_h-4),mausimaus,font)

    sidebar.setBgColor((0.0,0.0,0.5,0.1))

    clock = pygame.time.Clock()

    curLevel = STARTLEVEL



    #Hauptschleife:
    while not sidebar.isExitClicked():
        tools.clearScreen()

        ticktime = clock.tick(40)

        if sidebar.getMode() == hud.HUD_MODE_MAINMENU:

            #kleiner Effekt fuer die sidebar ;)

            x=mausimaus.getPos()[0]
            y=mausimaus.getPos()[1]

            if x > dinfo.current_w*FIELD_W_RATIO:
                x = dinfo.current_w*FIELD_W_RATIO
            r = 0.5-0.5/float(dinfo.current_w*FIELD_W_RATIO)*float(x)
            g = 0.5*float(y)/float(dinfo.current_h)
            b = float(x)/float(dinfo.current_w*FIELD_W_RATIO)

            sidebar.setBgColor((r,g,b,0.2))

            if sidebar.isPlayClicked():
                curLevel = STARTLEVEL
                sidebar.setMode(hud.HUD_MODE_PLAY)
                git.setLevel(curLevel)
                git.changeMode(gitter.MODE_SHOW)



                sidebar.setBgColor((0.0,0.0,0.3,0.2))

                sidebar.setMessage("Level " + str(curLevel))

        elif git.getMode() == gitter.MODE_SHOW:
            if git.readyToPlay():
                sidebar.setBgColor((0.3,0.0,0.1,0.2))
                git.changeMode(gitter.MODE_PLAY)
        elif git.getMode() == gitter.MODE_PLAY:
            if git.readyToShow():
                if git.madeMistake():
                    sidebar.setMode(hud.HUD_MODE_GAMEOVER)
                    sidebar.setBgColor((1.0,0.0,0.0,0.3))
                    sidebar.setMessage(str(curLevel-1) + " Level geschafft!")
                    git.changeMode(gitter.MODE_RANDOM)
                else:
                    curLevel += 1
                    if curLevel == gitter.GITTER_W*gitter.GITTER_H:
                        sidebar.setMode(hud.HUD_MODE_GAMEOVER)
                        sidebar.setMessage("alle Level geschafft!")
                        sidebar.setBgColor((0.0,1.0,0.0,0.3))
                        git.changeMode(gitter.MODE_RANDOM)
                    else:
                        git.setLevel(curLevel)
                        git.changeMode(gitter.MODE_SHOW)
                        sidebar.setBgColor((0.0,0.3,0.0,0.2))
                        sidebar.setMessage("Level " + str(curLevel))
        if sidebar.getMode() == hud.HUD_MODE_GAMEOVER:
            if sidebar.isOkClicked():
                sidebar.setMode(hud.HUD_MODE_MAINMENU)



        git.update()
        eventlist = eManager.getByType(KEYDOWN)
        for event in eventlist:
            if event.key == K_ESCAPE:
                exit()
        eManager.update()
        mausimaus.update()
        sidebar.update()

        tools.drawRect((0,0,dinfo.current_w,dinfo.current_h),0,(0,0,0,1))
        git.draw()
        sidebar.draw()

        pygame.display.flip()
