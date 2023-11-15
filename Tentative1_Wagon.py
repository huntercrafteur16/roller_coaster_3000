import os
import platform
import sys
from tkinter import Frame, TclError, Tk
import pygame
import pymunk
import pymunk.pygame_util
import random
random.seed(1)
import numpy as np
from pymunk.vec2d import Vec2d


def add_wagon(space,m,L):
    chassis = pymunk.Body(mass=m, moment=m)
    



def animate(): 
    
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0, 0*100)
    wagon_body = add_wagon(space,10,100)
    screen = pygame.display.set_mode((600,600))
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)

animate()
