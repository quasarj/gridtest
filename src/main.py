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

class MazeGame(object):
    theGrid = None

    def __init__(self):
        self.generateGrid()
        
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        
        self.windowSurfaceObj = pygame.display.set_mode((640,640))
        pygame.display.set_caption("GridTest")
        
        self.mousex, self.mousey = 0, 0
        
        self.posx, self.posy = 1, 1
        
        
        self.redDotObj = pygame.image.load('../res/red_dot.png')
        
        self.fontObj = pygame.font.SysFont("Sans", 32)
        
        self.winSound = pygame.mixer.Sound('../res/win.wav')

    def generateGrid(self):
        """Generate the grid, randomly"""
        
        # build the starting grid
        # this could be replaced with maze generation later
        self.theGrid = [[0 for i in range(32)] for i in range(32)]
        
        #fill with random walls
        for i in range(300):
            self.theGrid[random.randint(0, 31)][random.randint(0, 31)] = 1
        
        #enclose
        self.theGrid[0] = self.theGrid[31] = [1 for i in range(32)]
        for i in range(32):
            self.theGrid[i][0] = 1
            self.theGrid[i][31] = 1
        
        
        self.theGrid[1][1] = 0 #make sure top left corner is empty 

    def eventLoop(self):
        """The main event loop
        Basically everything is done here.
        """

        youwon = False

        while True: #pygame event loop
            if (self.posx, self.posy) == (30, 30) and not youwon:
                self.winSound.play()
                youwon = True
            
            self.windowSurfaceObj.fill(Color.white)
        
            # darw some rectangles
            for j in range(32):
                for i in range(32):
                    color = Color.white
                    
                    if self.posx == j and self.posy == i:
                        color = Color.green
                    elif self.theGrid[j][i] == 1:
                        color = Color.black
        
                    pygame.draw.rect(self.windowSurfaceObj, 
                                     color, 
                                     (i*20, j*20, 20, 20))
            
            
            
            msgSurfaceObj = self.fontObj.render("This is a test", 
                                                True, Color.blue)
            msgRectObj = msgSurfaceObj.get_rect()
            msgRectObj.topleft = (10, 20)
            self.windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)
            
        
            # blit the red dot at the cursor, but center it over the cursor
            self.windowSurfaceObj.blit(self.redDotObj, 
                                       (self.mousex - (self.redDotObj.get_width()//2), 
                                        self.mousey - (self.redDotObj.get_height()//2))) 
            
            
            
            # main event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == KEYDOWN:
                    youwon = False
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
        
                    elif event.key == K_r:
                        self.generateGrid()
        
                    elif event.key == K_d:
                        if self.theGrid[self.posx][self.posy + 1] == 0:
                            self.posy += 1
                            
                    elif event.key == K_a:
                        if self.theGrid[self.posx][self.posy - 1] == 0:
                            self.posy -= 1
                            
                    elif event.key == K_w:
                        if self.theGrid[self.posx - 1][self.posy] == 0:
                            self.posx -= 1
                            
                    elif event.key == K_s:
                        if self.theGrid[self.posx + 1][self.posy] == 0:
                            self.posx += 1
        
            pygame.display.update()
            self.fpsClock.tick(30) #limit at 30 fps
            
            
if __name__ == '__main__':
    game = MazeGame()
    game.eventLoop()