import pymunk.pygame_util
import pymunk
import pygame
import sys
import random
from pymunk import Vec2d
random.seed(1)

# Création du pendule


def wagon(space):
    wagon = pymunk.Body()
    wagon_shape = pymunk.Poly(
        wagon, [(-20, -20), (-20, 20), (20, 20), (20, -20)])
    wagon.position = (50, 50)
    wagon_shape.mass = 1
    wagon_shape.friction = 1
    space.add(wagon, wagon_shape)

    ligne = pymunk.Body(body_type=pymunk.Body.STATIC)
    ligne_shape1 = pymunk.Segment(ligne, [100, 200], [200, 400], 10)
    ligne_shape2 = pymunk.Segment(ligne, [200, 400], [400, 400], 10)
    ligne_shape3 = pymunk.Segment(ligne, [400, 400], [500, 200], 10)
    space.add(ligne, ligne_shape1, ligne_shape2, ligne_shape3)

    joint = pymunk.GrooveJoint(ligne, wagon, [100, 200], [200, 400], [0, 0])
    joint.collide_bodies = False
    space.add(joint)
    return

# main


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Wagon")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 100.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    wagon(space)

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


if __name__ == '__main__':
    main()
