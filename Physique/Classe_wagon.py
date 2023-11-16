from classes_travail_wagon import *
from pymunk.vec2d import Vec2d
import numpy as np
import pymunk
import sys
import pygame
import pymunk.pygame_util
import random
random.seed(1)


class wagon:
    """wagon(space, Mass, L, h, position_init) will create a wagon of mass M, lenght L,
      height h and starting position of the center of the body.Tension sets the force of the spring.
        For a flat line, choose position_init = (x, y_line-50 )

        Example wagon(space, 5, 100, 50, (300, 150)) will add a wagon to space"""

    def __init__(self, space, Mass: float, L: float, h: float, position_init: tuple, tension_ressort=500):

        Mass_roue, Mass_chassis = (1/3)*Mass, (2/3)*Mass
        Start_line(space, (position_init[0]-(L/2+10), position_init[1]+50),
                   (position_init[0]+L/2+10, position_init[1]+50))
        p = Vec2d(position_init[0], position_init[1])
        vs = [(-L/2, -h/2), (L/2, -h/2), (L/2, h/2), (-L/2, h/2)]
        v2, v3 = vs[2], vs[3]
        v4 = (0, h+50)
        v5 = (0, h/2)
        chassis = Poly(space, p, vs, Mass_chassis, L, h)
        wheel1 = Circle(space, p+v2, Mass_roue/2, L/6)
        wheel2 = Circle(space, p+v3,  Mass_roue/2, L/6)
        wheel3 = Circle(space, p+v4, 1, L/6)

        PivotJoint(space, chassis.body, wheel1.body, v2, (0, 0), False)
        PivotJoint(space, chassis.body, wheel2.body, v3, (0, 0), False)
        DampedSpring(space, chassis.body, wheel3.body,
                     v5, (0, 0), L/6, tension_ressort, 70)


d  # ef animate():

# clock = pygame.time.Clock()
# space = pymunk.Space()
# space.gravity = (0.0, 900)
# wagon(space, 5, 100, 50, (300, 150))
# screen = pygame.display.set_mode((600, 600))
# draw_options = pymunk.pygame_util.DrawOptions(screen)

# while True:
# for event in pygame.event.get():
# if event.type == pygame.QUIT:
# sys.exit(0)
# elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
# sys.exit(0)

# screen.fill((255, 255, 255))
# space.debug_draw(draw_options)
# space.step(1/50.0)
# pygame.display.flip()
# clock.tick(50)


# animate()
