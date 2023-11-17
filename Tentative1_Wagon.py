import pymunk.pygame_util
import pymunk
import pygame
import sys
import random
from pymunk import Vec2d
random.seed(1)

# Création du pendule


def add_wagon(space):
    wagon = pymunk.Body()
    wagon_shape = pymunk.Poly(
        wagon, [(-20, -20), (-20, 20), (20, 20), (20, -20)])
    wagon_shape.mass = 1
    wagon_shape.friction = 1
    wagon.velocity = (20, 0)
    space.add(wagon, wagon_shape)
    return wagon

# Création section parabole


def création_section(space):
    segments = {i: ([300 + i*10, 300 - 0.01*(i*10)**2], [300 +
                    (i+1)*10, 300 - 0.01*((i+1)*10)**2]) for i in range(-10, 11)}
    ligne = pymunk.Body(body_type=pymunk.Body.STATIC)
    space.add(ligne)
    for i, segment in segments.items():
        ligne_shape = pymunk.Segment(ligne, segment[0], segment[1], 5)
        space.add(ligne_shape)
    position_x_to_indice = {segments[i][0][0]: i for i in range(-10, 11)}
    return ligne, segments, position_x_to_indice

# Création de la liaison


def création_liaison(space, ligne, segments, wagon, i):
    joint = pymunk.GrooveJoint(
        ligne, wagon, segments[i][0], segments[i][1], [0, 0])
    joint.collide_bodies = False
    return joint

# main


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Wagon")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 50)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    wagon = add_wagon(space)
    ligne, segments, position_x_to_indice = création_section(
        space)
    joint = création_liaison(space, ligne, segments, wagon, -10)
    space.add(joint)
    update_position_x = segments[-10][1][0] - 3
    update_indice = -10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        if wagon.position[0] >= update_position_x:
            space.remove(joint)
            joint = création_liaison(
                space, ligne, segments, wagon, position_x_to_indice[update_position_x + 3])
            space.add(joint)
            update_indice += 1
            update_position_x = segments[update_indice][1][0] - 3

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
