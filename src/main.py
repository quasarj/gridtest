'''
Created on Oct 28, 2011

@author: QAJarosz
'''


import sys
import random

import pygame
from pygame.locals import *


class Color(object):
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)


def generateGrid():

    # build the starting grid
    # this could be replaced with maze generation later
    theGrid = [[0 for i in range(32)] for i in range(32)]
    
    #fill with random walls
    for i in range(200):
        theGrid[random.randint(0, 31)][random.randint(0, 31)] = 1
    
    #enclose
    theGrid[0] = theGrid[31] = [1 for i in range(32)]
    for i in range(32):
        theGrid[i][0] = 1
        theGrid[i][31] = 1
    
    
    theGrid[1][1] = 0 #make sure top left corner is empty 

    return theGrid

theGrid = generateGrid()

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,640))
pygame.display.set_caption("GridTest")

mousex, mousey = 0, 0

posx, posy = 1, 1


redDotObj = pygame.image.load('../res/red_dot.png')

fontObj = pygame.font.SysFont("Helvetica", 32)

winSound = pygame.mixer.Sound('../res/win.wav')


youwon = False


while True: #pygame event loop
    if (posx, posy) == (30, 30) and not youwon:
        winSound.play()
        youwon = True
    
    windowSurfaceObj.fill(Color.white)

    # darw some rectangles
    for j in range(32):
        for i in range(32):
            color = Color.white
            
            if posx == j and posy == i:
                color = Color.green
            elif theGrid[j][i] == 1:
                color = Color.black

            pygame.draw.rect(windowSurfaceObj, 
                             color, 
                             (i*20, j*20, 20, 20))
    
    
    
    msgSurfaceObj = fontObj.render("This is a test", True, Color.blue)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10, 20)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
    

    # blit the red dot at the cursor, but center it over the cursor
    windowSurfaceObj.blit(redDotObj, (mousex - (redDotObj.get_width()//2), 
                                      mousey - (redDotObj.get_height()//2))) 
    
    
    
    # main event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            
            
        elif event.type == KEYDOWN:
            youwon = False
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

            elif event.key == K_r:
                theGrid = generateGrid()

            elif event.key == K_d:
                if theGrid[posx][posy + 1] == 0:
                    posy += 1
            elif event.key == K_a:
                if theGrid[posx][posy - 1] == 0:
                    posy -= 1
            elif event.key == K_w:
                if theGrid[posx - 1][posy] == 0:
                    posx -= 1
            elif event.key == K_s:
                if theGrid[posx + 1][posy] == 0:
                    posx += 1

    pygame.display.update()
    fpsClock.tick(30) #limit at 30 fps