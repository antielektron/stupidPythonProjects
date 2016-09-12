import pygame
import sys
import math
import datetime

#Attribute der Uhr:---------------------------------------------------------------------------------
windowMargin = 30			#Abstand Uhr -> Fensterwand
windowWidth = 600
windowHeight = windowWidth
windowCenter = windowWidth/2, windowHeight/2
clockMarginWidth = 20
secondColor = (255,0,0)
minuteColor = (100,200,0)
hourColor = (100,200,0)
clockMarginColor = (130,130,0)
clockBackgroundColor = (20,40,30)
backgroundColor = (255,255,255)
hourCursorLength = windowWidth/2.0 - windowMargin -140
minuteCursorLength = windowWidth/2.0 - windowMargin - 40
secondCursorLength = windowWidth/2.0 - windowMargin - 10

virtualSpeed = 1
useVirtualTimer = False

pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('AnalogClock')
#Grundlegende Funktionen:---------------------------------------------------------------------------

#Funktion um die Position eines Zeiger zu ermitteln (0 Grad liegen auf 12 uhr!!!)
def getCursorPositionDegrees(position, scale):
	#offset von -90 grad um 0 grad bei 12 uhr zu haben:
	cursorOffset = -90
	degrees = 360.0 / scale * position + cursorOffset
	return degrees

#zur Umrechnung in Bogenmass:
def gradToBogenmass(degrees):
	return degrees/180.0*math.pi

#endpunkte der Zeiger berechnen:
def getCirclePoint(position, scale, cursorLength):
	degrees = getCursorPositionDegrees(position, scale)
	bogenmass = gradToBogenmass(degrees)
	xPos = round(math.cos(bogenmass)*cursorLength+windowCenter[0])
	yPos = round(math.sin(bogenmass)*cursorLength+windowCenter[1])
	return (xPos,yPos)
#Grafikfunktionen:----------------------------------------------------------------------------------
def drawBackground():
	screen.fill(backgroundColor)
	pygame.draw.ellipse(screen, clockMarginColor, (windowMargin, windowMargin, windowWidth-2*windowMargin, windowWidth-2*windowMargin))
	pygame.draw.ellipse(screen, clockBackgroundColor,(windowMargin+clockMarginWidth/2,
		windowMargin+clockMarginWidth/2, windowWidth-(windowMargin+clockMarginWidth/2)*2,
		windowWidth-(windowMargin+clockMarginWidth/2)*2))

def drawForeground():
	pygame.draw.ellipse(screen,clockMarginColor,(windowWidth/2.0-9, windowHeight/2.0-9, 18, 18))

def drawCursor(color, width, length, position, scale):
	end = getCirclePoint(position, scale, length)
	pygame.draw.line(screen, color, windowCenter, end, width)

def drawCurrentTime():
	if useVirtualTimer:
		global hour, minute, second, micro
		timeGoesOn()
	else:
		now = datetime.datetime.now()
		micro = now.microsecond
		hour = now.hour
		minute = now.minute
		second = now.second

	drawCursor(hourColor,15,hourCursorLength,hour+minute/60.0, 12)
	drawCursor(minuteColor, 8, minuteCursorLength, minute+second/60.0, 60)
	drawCursor(secondColor, 3, secondCursorLength, second+micro/1000000.0,60)
#Enventhandling:------------------------------------------------------------------------------------
def handleEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			sys.exit(0)
#die Main:------------------------------------------------------------------------------------------
def main():
	#Hauptschleife:
	while True:
		handleEvents()
		screen.fill(backgroundColor)

		drawBackground()
		drawCurrentTime()
		drawForeground()

		pygame.display.flip()
		pygame.time.delay(10)

if __name__ == '__main__':
	main()