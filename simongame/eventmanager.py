import pygame
from pygame.locals import *

class eventmanager(object):
    def __init__(self):
        self.eventlist = []

    def update(self):
        self.eventlist = pygame.event.get()

    def getAll(self):
        return self.eventlist

    def getByType(self,Type):
        list = []
        for event in self.eventlist:
            if event.type == Type:
                list.append(event)

        return list

