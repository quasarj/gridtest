'''
Created on Oct 28, 2011

@author: QAJarosz
'''

MSIZE = 33  # MSIZE must always be an odd number!
BSIZE = 20

import sys
import random

import pygame
from pygame.locals import *

import numpy
from numpy.random import random_integers as rnd

from example import maze as example_maze

class Color(object):
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)

class MazeGame(object):
    theGrid = None
    walls = None
    maze_func = None

    def __init__(self, maze_function):
        self.maze_func = maze_function
        self.drawMaze()
        
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        
        self.windowSurfaceObj = pygame.display.set_mode((MSIZE * BSIZE, 
                                                         MSIZE * BSIZE))
        pygame.display.set_caption("GridTest")
        
        self.mousex, self.mousey = 0, 0
        
        self.posx, self.posy = 1, 1
        
        
        self.redDotObj = pygame.image.load('../res/red_dot.png')
        
        self.fontObj = pygame.font.SysFont("Sans", 32)
        
        self.winSound = pygame.mixer.Sound('../res/win.wav')

    def drawMaze(self):
        self.theGrid = self.maze_func(MSIZE, MSIZE)

    def eventLoop(self):
        """The main event loop
        Basically everything is done here.
        """

        youwon = False

        while True: #pygame event loop
            if (self.posx, self.posy) == (MSIZE - 2, MSIZE - 2) and not youwon:
                self.winSound.play()
                youwon = True
            
            self.windowSurfaceObj.fill(Color.white)
        
            # darw some rectangles
            for j in range(MSIZE):
                for i in range(MSIZE):
                    color = Color.white
                    
                    if self.posx == j and self.posy == i:
                        color = Color.green
                    #elif (j, i) in self.walls:
                    elif self.theGrid[j,i] == 1:
                        color = Color.black
        
                    pygame.draw.rect(self.windowSurfaceObj, 
                                     color, 
                                     (i*BSIZE, j*BSIZE, BSIZE, BSIZE))
            
            
            
#            msgSurfaceObj = self.fontObj.render("This is a test", 
#                                                True, Color.blue)
#            msgRectObj = msgSurfaceObj.get_rect()
#            msgRectObj.topleft = (10, 20)
#            self.windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
            
        
            # blit the red dot at the cursor, but center it over the cursor
#            self.windowSurfaceObj.blit(self.redDotObj, 
#                                       (self.mousex - (self.redDotObj.get_width()//2), 
#                                        self.mousey - (self.redDotObj.get_height()//2))) 
            
            
            
            # main event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == KEYDOWN:
                    youwon = False
                    if event.key == K_ESCAPE or event.key == K_q:
                        pygame.event.post(pygame.event.Event(QUIT))
        
                    elif event.key == K_r:
                        self.drawMaze()

            keys = pygame.key.get_pressed()
            if keys[K_d]:
                if not self.theGrid[self.posx, self.posy + 1]:
                    self.posy += 1
                    
            if keys[K_a]:
                if not self.theGrid[self.posx, self.posy - 1]:
                    self.posy -= 1
                    
            if keys[K_w]:
                if not self.theGrid[self.posx - 1, self.posy]:
                    self.posx -= 1
                    
            if keys[K_s]:
                if not self.theGrid[self.posx + 1, self.posy]:
                    self.posx += 1

            pygame.display.update()
            self.fpsClock.tick(30) #limit at 30 fps
            
            
if __name__ == '__main__':
    game = MazeGame(example_maze)
    game.eventLoop()