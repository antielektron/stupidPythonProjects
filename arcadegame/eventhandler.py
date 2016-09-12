import pygame
from pygame.locals import *
from sys import exit

if __name__ == '__main__':
    pygame.init()


#modul, welches Werkzeuge enthaelt, die zur eventbearbeitung dienen.
KEY_INACTIVE = 0
KEY_PRESSED = 1
KEY_HOLD = 2
KEY_RELEASED = 3

class EventHandler(object):
    def __init__(self):
        self.eventlist = []
        
    
    def update(self):
        
        
        self.eventlist = pygame.event.get()
        
            
    
    def getEventList(self):
        return self.eventlist


class KeyHandler(object):
    
    def __init__(self):
        self.keyDict = {}
        
    
    def registerKey(self,keycode):
        self.keyDict[keycode] = KEY_INACTIVE
    
    def getKeyState(self,keycode):
        
        code = self.keyDict[keycode]
        
        if code == KEY_PRESSED:
            self.keyDict[keycode] = KEY_HOLD
        elif code == KEY_RELEASED:
            self.keyDict[keycode] = KEY_INACTIVE
        return code
    
    def update(self, e_handler):
        
        eventlist = e_handler.getEventList()
        
        #TODO: hier ist noch optimierungsbedarf, was die Geschwindigkeit angeht...
        for event in eventlist:
            
            #I love verschachtelte if's ;)
            if event.type == KEYUP or event.type == KEYDOWN:
                if self.keyDict.has_key(event.key):
                    
                    if self.keyDict[event.key] == KEY_INACTIVE:
                        if event.type == KEYDOWN:
                            self.keyDict[event.key] = KEY_PRESSED
                    
                    elif  self.keyDict[event.key] == KEY_HOLD:
                        if event.type == KEYUP:
                            self.keyDict[event.key] = KEY_RELEASED
                            
            
        

#klasse eig unnoetig, da pygame diese viel bequemer selber bereitstellt...
class MouseHandler(object):
    
    def __init__(self):
        self.mouseX = 0;
        self.mouseY = 0;
        self.LeftButton = KEY_INACTIVE
        self.MiddleButton = KEY_INACTIVE
        self.RightButton = KEY_INACTIVE
        self.isMouseMoved = False
    
    def update(self, e_handler):
        elist = e_handler.getEventList()
        
        
        for event in elist:
            if event.type == MOUSEMOTION:
                self.mouseX, self.mouseY = event.pos
                self.isMouseMoved = True
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.LeftButton == KEY_INACTIVE:
                        self.LeftButton = KEY_PRESSED
                elif event.button == 2:
                    if self.MiddleButton == KEY_INACTIVE:
                        self.MiddleButton = KEY_PRESSED
                elif event.button == 3:
                    if self.RightButton == KEY_INACTIVE:
                        self.RightButton = KEY_PRESSED
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.LeftButton == KEY_HOLD:
                        self.LeftButton = KEY_RELEASED
                elif event.button == 2:
                    if self.MiddleButton == KEY_HOLD:
                        self.MiddleButton = KEY_RELEASED
                elif event.button == 3:
                    if self.RightButton == KEY_HOLD:
                        self.RightButton = KEY_RELEASED
    
    def getLeftButtonState(self):
        code = self.LeftButton
        
        if code == KEY_PRESSED:
            self.LeftButton = KEY_HOLD
        elif code == KEY_RELEASED:
            self.LeftButton = KEY_INACTIVE
        return code
    
    def getMiddleButtonState(self):
        code = self.MiddleButton
        
        if code == KEY_PRESSED:
            self.MiddleButton = KEY_HOLD
        elif code == KEY_RELEASED:
            self.MiddleButton = KEY_INACTIVE
        return code
    
    def getRightButtonState(self):
        code = self.RightButton
        
        if code == KEY_PRESSED:
            self.RightButton = KEY_HOLD
        elif code == KEY_RELEASED:
            self.RightButton = KEY_INACTIVE
        return code
    
    def mouseMoved(self):
        if self.isMouseMoved:
            self.isMouseMoved = False
            return True
        return False
    
    def getMouseX(self):
        return self.mouseX
    
    def getMouseY(self):
        return self.mouseY
    
    def getMousePos(self):
        return (self.mouseX, self.mouseY)


    

if __name__ == '__main__':
    
    font = pygame.font.SysFont("arial", 16);
    
    elist = EventHandler()
    test = KeyHandler()
    mouse = MouseHandler()
    
    screen = pygame.display.set_mode(( 800, 600),0,32);

    
    test.registerKey(K_UP)
    test.registerKey(K_DOWN)
    
    while True:
        
        screen.fill((255, 255, 255))
        elist.update();
        test.update(elist)
        mouse.update(elist)
        
        code = test.getKeyState(K_UP)
        code2 = test.getKeyState(K_DOWN)
        moved = mouse.mouseMoved()
        
        button = mouse.getLeftButtonState()
        
        pos = mouse.getMousePos()
        
        
        
        if code == KEY_RELEASED:
            exit();
        
        screen.blit( font.render('KeyUp: '+str(code), True, (0, 0, 0)), (0, 0) )
        screen.blit( font.render('KeyDown: '+str(code2), True, (0, 0, 0)), (0, 20) )
        screen.blit( font.render('Maus: '+str(moved), True, (0, 0, 0)), (0, 40) )
        screen.blit( font.render('Maus: '+str(button), True, (0, 0, 0)), (0, 60) )
        screen.blit( font.render('Maus: '+str(pos), True, (0, 0, 0)), (0, 80) )
        pygame.display.update()



        