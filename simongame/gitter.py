import pygame
import random
from pygame.locals import *
import tools
import kachel
from maus import *
import eventmanager
import FTGL
import button

#Groesse des Spielfeldes
GITTER_W = 7
GITTER_H = 5

#GitterModi:
MODE_RANDOM = 0
MODE_SHOW = 1
MODE_PLAY = 2

#Werte fuer den Random Mode:

RANDOM_FRAMES = 60      #Anzahl der Frames fuer eine einzelne Sequenz
RANDOM_ELEMENT_RANGE =GITTER_W*GITTER_H/4 #Wie viele Elemente werden Maximal zufaellig aktiviert (muss kleinergleich sein als Gitter_W*Gitter_H)

#Werte fuer den Show Mode:

TIME_FACTOR = 0.9
MIN_STEPTIME = 20

COOLDOWNTIME = 20


class gitter(object):
    def __init__(self,size,eManager,mouse,sounds):
        self.kachelarray = []

        self.size = size

        self.eManager = eManager
        
        self.kachelW = size[0]/GITTER_W
        self.kachelH = size[1]/GITTER_H

        self.sounds = sounds

        self.mode = MODE_RANDOM

        #Variablen fuer den MODE_RANDOM
        self.randomFrame = 0
        self.randomSequence = [] #wird auch fuer alle anderen Sequenzen verwendet

        self.mausimaus = mouse
      
        for x in range(GITTER_W*GITTER_H):
            self.kachelarray.append( kachel.kachel(x%GITTER_W,x//GITTER_W,self.kachelW,self.kachelH))

        self.initRandomSequence()

        #Variablen fuer den Play Mode:
        self.level = 1
        self.mistake = False
        self.playingStep = 0
        self.done = False

        #Variablen fuer den Show Mode:        
        self.curFrame = 0
        self.maxFrame = MIN_STEPTIME

        self.showing = False

        self.cooldown = COOLDOWNTIME



    
    def getIndex(self,pos):
        return pos[1]*GITTER_W + pos[0]
    
    def getPos(self,index):
        return (index%GITTER_W,index//GITTER_W)

    def deactivateAll(self):
        for kachel in self.kachelarray:
            kachel.deactivate()

    def activateAll(self):
        for kachel in self.kachelarray:
            kachel.activate()

    def setLevel(self,level):
        self.level = level

    def initRandomSequence(self):
        self.randomFrame = 0

        #alle deaktivieren:
        self.deactivateAll()

        #erzeuge eine sequenz aus kachelindizies, die 1 bis RANDOM_ELEMENT_RANGE lang ist
        self.randomSequence = random.sample(range(GITTER_W*GITTER_H),random.randint(1,RANDOM_ELEMENT_RANGE))

        #die in der random sequenz aktivieren:
        for i in self.randomSequence:
            self.kachelarray[i].activate()

    def generatePlaySequence(self,level):
        self.randomSequence = random.sample(range(GITTER_W*GITTER_H),level)

    def changeMode(self,mode):
        self.mode = mode

        if mode == MODE_RANDOM:
            self.randomFrame = 0

            #noch kurz die richtige Loesung zeigen:
            self.deactivateAll()
            for i in self.randomSequence:
                self.kachelarray[i].activate()

        elif mode == MODE_SHOW:
            self.done = False
            self.cooldown = COOLDOWNTIME
            self.showing = True
            self.generatePlaySequence(self.level) #level sollte also vorher gesetzt werden !!!
            self.curFrame = 0
            self.maxFrame = MIN_STEPTIME + (TIME_FACTOR*MIN_STEPTIME)*self.level
            self.activateAll()
            self.sounds[1].play()


        elif mode == MODE_PLAY:
            self.cooldown = COOLDOWNTIME
            self.mistake = False
            self.playingStep = 0
            self.activateAll()
            self.sounds[1].play()


        else:
            pass #TODO: System fuer einheitliche Fehlermeldungen implementieren
        
    def getMode(self):
        return self.mode

    def readyToPlay(self):
        return not self.showing

    def readyToShow(self):
        return self.done

    def madeMistake(self):
        return self.mistake

    def inSequence(self,kachel):
        
        for i in range(self.level):
            if self.getIndex(kachel.getPos()) == self.randomSequence[i]:
                return True
        return False


    
    def update(self):

        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.deactivateAll()

            #und die kachel updaten:
            for kachel in self.kachelarray:
                kachel.update()
        else:
                
            for kachel in self.kachelarray:
                kachel.deselect()
                kPos = kachel.getPos()
                
                mausPos = self.mausimaus.getPos()

                mousePressed = self.mausimaus.getState(0) == BUTTON_PRESSED

                #WARNUNG: nicht in den verschachtelungen verirren!!!
                if not self.mode == MODE_SHOW:
                    if tools.is2DPointCollision(mausPos,(kPos[0]*kPos[2],kPos[1]*kPos[3],kPos[2],kPos[3])):
                        if not kachel.isActive:
                            if mousePressed:

                                kachel.activate()

                                if self.mode == MODE_PLAY:
                                    if self.inSequence(kachel):
                                        self.playingStep += 1
                                        self.sounds[0].play()
                                        if self.playingStep == self.level:
                                            self.done = True
                                            
                                    else:
                                        self.mistake = True
                                        self.sounds[2].play()
                                        self.done = True
                            else:
                                kachel.select()
                
                kachel.update()

            if self.mode == MODE_RANDOM:

                self.randomFrame += 1
                if self.randomFrame > RANDOM_FRAMES:
                    self.initRandomSequence()


            elif self.mode == MODE_SHOW:
                self.curFrame +=1
                if self.curFrame >= self.maxFrame:
                    self.showing = False

                for i in self.randomSequence:
                    self.kachelarray[i].activate()


            
        
    def draw(self):
        for kachel in self.kachelarray:
            kachel.draw()
