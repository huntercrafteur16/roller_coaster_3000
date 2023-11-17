from wagon import *
from tkinter import GROOVE
from classes_travail_wagon import *
from pymunk.vec2d import Vec2d
import numpy as np
import pymunk
import sys
import pygame
import pymunk.pygame_util
import random
random.seed(1)


class Lien:
    def __init__(self, space, locomotive, wagon):
        L1 = locomotive.L
        L2 = wagon.L
        point_attache_loc = (-(4*L1/6), 0)
        point_attache_wag = ((4*L2/6), 0)
        PinJoint(space, locomotive.c, wagon.c,
                 point_attache_loc, point_attache_wag)


space = pymunk.Space()
pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
space.gravity = (0.0, 9.81*100)

Wagon1 = Wagon(space, 1000, 150, 50, (340, 100), 80000)
Wagon2 = Wagon(space, 1000, 150, 50, (80, 100), 80000)
Lien(space, Wagon1, Wagon2)
Start_line(space, (-100, 140), (1200, 160))

draw_options = pymunk.pygame_util.DrawOptions(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    space.step(1/500.0)
    pygame.display.flip()
    clock.tick(500)
