from PIL import Image
from PIL import ImageDraw

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


class Kachel:

    def __init__(self, pos, size):
        self.dirs = [False, False, False, False]
        self.visited = False
        self.pos = pos
        self.size = size
        self.walkable = False

    def isVisited(self):
        return self.visited

    def getPos(self):
        return self.pos

    def open(self, direction):
        self.dirs[direction] = True

    def isOpen(self, direction):
        return self.dirs[direction]

    def touch(self):
        self.visited = True

    def makeWalkable(self):
        self.walkable = True

    def isWalkable(self):
        return self.walkable

    def getNumberOfOpenWays(self):
        n = 0
        for i in self.dirs:
            if i:
                n += 1

        return n

    def getArrayOfClosedWays(self):
        result = []
        for i in range(4):
            if not self.dirs[i]:
                result.append(i)
        return result

    def draw(self, target, offset):

        pos = [(self.pos[0] * self. size[0] + offset[0],
            self.pos[1] * self.size[1] + offset[1]),
            ((self.pos[0] + 1) * self.size[0] + offset[0],
            self.pos[1] * self.size[1] + offset[1]),
            ((self.pos[0] + 1) * self.size[0] + offset[0],
            (self.pos[1] + 1) * self.size[1] + offset[1]),
            (self.pos[0] * self.size[0] + offset[0],
            (self.pos[1] + 1) * self.size[1] + offset[1])]

        if (not self.dirs[NORTH]):
            target.line((pos[0], pos[1]), (0, 0, 0))

        if (not self.dirs[EAST]):
            target.line((pos[1], pos[2]), (0, 0, 0))

        if (not self.dirs[SOUTH]):
            target.line((pos[2], pos[3]), (0, 0, 0))

        if (not self.dirs[WEST]):
            target.line((pos[3], pos[0]), (0, 0, 0))

