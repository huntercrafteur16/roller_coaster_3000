from pymunk.vec2d import Vec2d
import numpy as np
import os
import platform
import sys
from tkinter import Frame, TclError, Tk
import pygame
import pymunk
import pymunk.pygame_util
import random
random.seed(1)


def add_wagon(space, m, L):
    ligne = pymunk.Body(body_type=pymunk.Body.STATIC)
    ligne_shape = pymunk.Segment(ligne, (0, 300), (600, 300), 8)

    wagon = pymunk.Body()
    wagon_shape = pymunk.Poly(wagon, [(-5, -5), (5, -5), (5, 5), (-5, 5)])
    space.add(ligne, ligne_shape, wagon, wagon_shape)
    return


def animate():

    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0.0, 900)
    screen = pygame.display.set_mode((600, 600))
    wagon_body = add_wagon(space, 10, 100)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)


animate()
