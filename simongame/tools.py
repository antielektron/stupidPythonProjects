import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import FTGL

#Opengl-Tools:------------------------------------------------------------------

def clearScreen():
    glClearColor(0.0,0.0,0.0,0.0)

def GlInit():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, height, 0.0, -6.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def drawRect(rect, depth,color):
    glBegin(GL_QUADS)
    glColor4f(color[0],color[1],color[2],color[3])

    glVertex3f(rect[0],rect[1],depth)
    glVertex3f(rect[0]+rect[2],rect[1],depth)
    glVertex3f(rect[0]+rect[2],rect[1]+rect[3],depth)
    glVertex3f(rect[0],rect[1]+rect[3],depth)

    glEnd()

#FTGL-Tools:--------------------------------------------------------------------
def loadFont(filename,facesize):
    font = FTGL.TextureFont(filename)
    font.FaceSize(facesize[0],facesize[1])
    return font

def writePerFTGL(string,font,pos,color):
    #glOrtho(0.0, glOrthoSize[0], 0.0, glOrthoSize[1], -6.0, 0.0)
    
    glPushMatrix()
    glColor4f(color[0],color[1],color[2],color[3])
    #so ein bissl die Matrix drehen, damit der Text nicht aufm Kopf steht :D
    glTranslatef(pos[0], pos[1], 0.0)
    glRotate(180,0.0,0.0,1.0)
    glRotate(180,0.0,1.0,0.0)
    #und rendern:
    glRasterPos(0, 0)
    font.Render(string)
    #und die Matrix wieder loeschen
    glPopMatrix()

#Kollisionsabfragen:------------------------------------------------------------

def is2DPointCollision(point, rect):
    if point[0] <= rect[0] or point[0] >= rect[0]+rect[2]:
        return False
    elif point[1] <= rect[1] or point[1] >= rect[1] + rect[3]:
        return False
    return True


if __name__ == "__main__":
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF | FULLSCREEN
    pygame.display.set_mode((800,600),video_flags)
    resize((800,600))
    clearScreen()

    clock = pygame.time.Clock()
    
    #Hauptschleife:
    while True:
        
        
        ticktime = clock.tick(20)
        #print ticktime
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
       
        
        drawRect((0,0,200,200),0,(1,1,1,1))
        
        pygame.display.flip()




