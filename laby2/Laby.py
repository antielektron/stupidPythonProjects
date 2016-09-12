#!/usr/bin/python
from Kachel import *
from PIL import Image
from PIL import ImageDraw
import random
import sys
import math

CHAR_WALL = "X"
CHAR_START = "*"
CHAR_END = "#"


class Laby:

    def __init__(self, size, arraySize, kachelSize, waySteps):
        self.kachelArray = []
        self.size = size
        self.arraySize = arraySize
        self.kachelSize = kachelSize
        self.img = None
        self.drawObject = None
        self.createImage()
        self.createArray()
        self.visitedFields = 0

        self.maxWaysteps = waySteps    # ein aenderung dieses wertes duerfte
                                       # den schwierigkeitsgrad beeinflussen

    def createImage(self):
        self.img = Image.new("RGB", (self.size[0], self.size[1]),
            (255, 255, 255))
        self.drawObject = ImageDraw.ImageDraw(self.img)

    def createArray(self):
        for x in range(self.arraySize[0]):
            tmp = []
            for y in range(self.arraySize[1]):
                tmp.append(Kachel((x, y), self.kachelSize))

            self.kachelArray.append(tmp)

    def makeAllWalkable(self):
        for y in self.kachelArray:
            for x in y:
                x.makeWalkable()

    

    def draw(self):
        for i in self.kachelArray:
            for j in i:
                j.draw(self.drawObject, self.kachelSize)
    
    def saveToTxt(self, filename):
        fobj = open(filename, "w")
        for j in range(self.arraySize[0]*2 + 1):
            fobj.write(CHAR_WALL)
        fobj.write("\n")
        for i in range(self.arraySize[1]):
            fobj.write(CHAR_WALL)
            for j in range(self.arraySize[0]):
                if (i == 0 and j == 0):
                    fobj.write(CHAR_START)
                elif(i == self.arraySize[1]-1 and j == self.arraySize[0]-1):
                    fobj.write(CHAR_END)
                else:
                    fobj.write(" ")
                
                if self.kachelArray[j][i].isOpen(EAST):
                    fobj.write(" ")
                else:
                    fobj.write(CHAR_WALL)
                
            fobj.write("\n" + CHAR_WALL)
            for j in range(self.arraySize[0]):
                if self.kachelArray[j][i].isOpen(SOUTH):
                    fobj.write(" ")
                else:
                    fobj.write(CHAR_WALL)
                
                fobj.write(CHAR_WALL)
            
            fobj.write("\n")
        
        fobj.close();

    def showOnScreen(self):

        self.img.show()

    def save(self, filename):
        self.img.save(filename)

    def openWay(self, pos, direction):
        self.kachelArray[pos[0]][pos[1]].open(direction)

        if direction == NORTH:
            if pos[1] > 0:
                self.kachelArray[pos[0]][pos[1] - 1].open(SOUTH)
        elif direction == EAST:
            if pos[0] < self.arraySize[0] - 1:
                self.kachelArray[pos[0] + 1][pos[1]].open(WEST)
        elif direction == SOUTH:
            if pos[1] < self.arraySize[1] - 1:
                self.kachelArray[pos[0]][pos[1] + 1].open(NORTH)
        elif direction == WEST:
            if pos[0] > 0:
                self.kachelArray[pos[0] - 1][pos[1]].open(EAST)

    def scanNeighbours(self, scanPos):
        scanResult = [0, 0, 0, 0]  # 0 = nix, 1 = unbesucht, 2 = besucht
        # NORTH:
        if scanPos[1] > 0:
            north = self.kachelArray[scanPos[0]][scanPos[1] - 1]
            if north.isWalkable():
                if north.isVisited():
                    scanResult[NORTH] = 2
                else:
                    scanResult[NORTH] = 1
        # SOUTH:
        if scanPos[1] < self.arraySize[1] - 1:
            south = self.kachelArray[scanPos[0]][scanPos[1] + 1]
            if south.isWalkable():
                if south.isVisited():
                    scanResult[SOUTH] = 2
                else:
                    scanResult[SOUTH] = 1
        # WEST:
        if scanPos[0] > 0:
            west = self.kachelArray[scanPos[0] - 1][scanPos[1]]
            if west.isWalkable():
                if west.isVisited():
                    scanResult[WEST] = 2
                else:
                    scanResult[WEST] = 1
        # EAST:
        if scanPos[0] < self.arraySize[0] - 1:
            east = self.kachelArray[scanPos[0] + 1][scanPos[1]]
            if east.isWalkable():
                if east.isVisited():
                    scanResult[EAST] = 2
                else:
                    scanResult[EAST] = 1

        return scanResult

    def bakeWay(self, startPos):
        self.pos = startPos
        for c in range(self.maxWaysteps):   # pro weg maximal waysteps schritte

            self.kachelArray[self.pos[0]][self.pos[1]].touch()
            self.visitedFields += 1
            neighbours = self.scanNeighbours(self.pos)
            if neighbours.count(1) == 0:
                break

            possibleDirections = []
            for i in range(4):
                if neighbours[i] == 1:
                    possibleDirections.append(i)

            #zufaellige richtung waehlen:
            nextDir = random.sample(possibleDirections, 1)[0]
            self.openWay(self.pos, nextDir)

            #zur naechsten Kachel gehen:
            if nextDir == NORTH:
                self.pos = (self.pos[0], self.pos[1] - 1)

            elif nextDir == EAST:
                self.pos = (self.pos[0] + 1, self.pos[1])

            elif nextDir == SOUTH:
                self.pos = (self.pos[0], self.pos[1] + 1)

            elif nextDir == WEST:
                self.pos = (self.pos[0] - 1, self.pos[1])

    def bakeLaby(self, startPos, isFirstBake):
        if isFirstBake:
            print("Berechne Labyrinth...")
            self.bakeWay(startPos)
        unvisitedCounter = (self.arraySize[0]*self.arraySize[1]
            - self.visitedFields)

        while unvisitedCounter > 0:
            #fortschritt in Prozent
            print(str(float(self.visitedFields * 100.0)
                / float(self.arraySize[0] * self.arraySize[1])) + "%")
            # zaehle unbesuchte, an besuchten Feldern angrenzende Felder
            neighbours = []
            unvisitedCounter = 0
            for y in self.kachelArray:
                for x in y:
                    if not x.isVisited():

                        if self.scanNeighbours(x.getPos()).count(2) > 0:
                            unvisitedCounter += 1
                            neighbours.append(x)

            if unvisitedCounter > 0:
                nextPos = random.sample(neighbours, 1)[0]
                tmp = self.scanNeighbours(nextPos.getPos())
                possibleConnectDirs = []
                for i in range(4):
                    if tmp[i] == 2:
                        possibleConnectDirs.append(i)

                connectDir = random.sample(possibleConnectDirs, 1)[0]
                self.openWay(nextPos.getPos(), connectDir)
                self.bakeWay(nextPos.getPos())

if __name__ == "__main__":

    #programmaufruf: Laby.py [W] [H] [Feldgroesse] [filename]

    try:
        KACHELSIZE = int(sys.argv[3])
        WIDTH = int(sys.argv[1])
        HEIGHT = int(sys.argv[2])
        FILENAME = sys.argv[4]

    except:
        print("\nFehlerhafte Parameter!")
        print("Benoetigte Parameter:"
            + "[BREITE] [HOEHE] [FELDGROESSE] [DATEINAME] <WAYSTEPS>"
            + "\n\nBREITE: die Breite des Labyrinthes in Anzahl an Feldern"
            + "\n\nHOEHE: die Hoehe des Labyrinthes in Anzahl an Feldern"
            + "\n\nFELDGROESSE: Kantenlaenge eines Feldes in Pixeln"
            + "\n\nDATEINAME: Dateiname fuer das fertige Labyrinth (ohne dateiendung)"
            + "\n\nWAYSTEPS(optional): gibt die maximale Laenge eines "
            + "\nWegstuecks in Feldern an, die ohne Abzweigung vom Algorithmus"
            + "\ngeneriert werden kann. Pauschal kann man sagen: je kleiner "
            + "\nder Wert, desto kuerzer ist der kuerzeste Weg zwischen zwei "
            + "\nPunkten im Labyrinth. Standardwert ist 100 \n")

        sys.exit(0)

    # optionale Argumente:
    try:
        WAYSTEPS = int(sys.argv[5])
    except:
        WAYSTEPS = 100

    laby = Laby(((WIDTH + 2) * KACHELSIZE, (HEIGHT + 2) * KACHELSIZE),
        (WIDTH, HEIGHT), (KACHELSIZE, KACHELSIZE), WAYSTEPS)
    laby.makeAllWalkable()
    laby.bakeLaby((0, 0),True)
    laby.saveToTxt(FILENAME + ".txt")
    laby.openWay((0, 0), WEST)
    laby.openWay((WIDTH - 1, HEIGHT - 1), EAST)
    laby.draw()
    laby.save(FILENAME + ".png")
    laby.showOnScreen()
