import pymunk
import os
import platform
import sys
import pygame
import pymunk.pygame_util
import random
random.seed(1)
import numpy as np
from pymunk.vec2d import Vec2d


def add_wagon(space,m,L):
    ligne = pymunk.Body(mass=1, moment=1000, body_type= pymunk.Body.STATIC)
    ligne_shape = pymunk.Segment(ligne, (0, 176), (200, 176), 8)


    chassis = pymunk.Body(mass=m, moment=m)
    chassis_shape = pymunk.Poly.create_box(chassis,(L,L))
    chassis.position = (100,100)
    roue1 = pymunk.Body(mass=1, moment=1)
    roue2 = pymunk.Body(mass=1, moment=1)
    roue1.position = (100-45, 100+45)
    roue2.position = (100+45, 100+45)
    roue3 = pymunk.Body(mass=1, moment=1)
    roue4 = pymunk.Body(mass=1, moment=1)
    roue1_shape = pymunk.Circle(roue1, radius = 25)
    roue2_shape = pymunk.Circle(roue2, radius = 25)

    roue1_shape.filter = pymunk.ShapeFilter(group=1)
    roue2_shape.filter = pymunk.ShapeFilter(group=1)
    chassis_shape.filter = pymunk.ShapeFilter(group=1)


    roue3_shape = pymunk.Circle(roue3, radius = 15)
    roue4_shape = pymunk.Circle(roue4, radius = 15)
    joint02 = pymunk.PivotJoint(chassis, roue2, roue2.position)
    joint01 = pymunk.PivotJoint(chassis, roue1,roue1.position)
    
    space.add(joint01, joint02, roue1, roue2, roue1_shape, roue2_shape, chassis, chassis_shape, ligne, ligne_shape)


def animate(): 
    
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0, 1*100)
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
