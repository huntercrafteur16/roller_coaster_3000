import pymunk
import sys
import pygame
import pymunk.pygame_util
import random
random.seed(1)
import numpy as np
from pymunk.vec2d import Vec2d
from classes import *

def add_wagon(space,m, L):

    Box(space)
    p = Vec2d(200, 150)
    vs = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
    v0, v1, v2, v3 = vs
    v4 = (0,70)
    v5 = (0,30)
    chassis = Poly(space,p, vs)


    wheel1 = Circle(space,p+v2)
    wheel2 = Circle(space,p+v3)
    wheel3 = Circle(space, p+v4)

    PivotJoint(space,chassis.body, wheel1.body, v2, (0, 0), False)

    PivotJoint(space,chassis.body, wheel2.body, v3, (0, 0), False)

    DampedSpring(space, chassis.body, wheel3.body,v5,(0,0),1,700,1)
    


def animate(): 
    
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0, 900)
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
