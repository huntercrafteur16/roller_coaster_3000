import pymunk.pygame_util
import pymunk
import pygame
import sys
import random
from pymunk import Vec2d
import numpy as np
random.seed(1)

# chemin


def chemin(i):
    return - 0.1*np.exp(5 + 0.2*i)

# norme


def norme(p): return np.sqrt(p[0]**2 + p[1]**2)

# Création du pendule


def add_wagon(space):
    wagon = pymunk.Body()
    wagon_shape = pymunk.Poly(
        wagon, [(-20, -20), (-20, 20), (20, 20), (20, -20)])
    wagon_shape.mass = 1
    wagon_shape.friction = 0
    space.add(wagon, wagon_shape)
    return wagon

# Création section parabole


def création_section(space):
    # création des segments qui linéarisent une parabole
    segments = {i: ((300 + i*20, 300 + chemin(i)), (300 +
                    (i+1)*20, 300 + chemin(i+1))) for i in range(-10, 11)}
    ligne = pymunk.Body(body_type=pymunk.Body.STATIC)
    space.add(ligne)
    for i, segment in segments.items():
        ligne_shape = pymunk.Segment(ligne, segment[0], segment[1], 5)
        space.add(ligne_shape)
    # création d’un dict pour connaître l’indice d’une positon donnée
    p_to_i_gauche = {segments[i][0]: i for i in range(-10, 11)}
    p_to_i_droite = {segments[i][1]: i for i in range(-10, 11)}
    return ligne, segments, p_to_i_gauche, p_to_i_droite

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
    space.gravity = (0.0, 300)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # création des objets

    wagon = add_wagon(space)
    wagon.velocity = Vec2d(150, 0)
    ligne, segments, p_to_i_gauche, p_to_i_droite = création_section(
        space)
    joint = création_liaison(space, ligne, segments, wagon, -10)
    space.add(joint)

    # initialisation des paramètres

    update_indice = -9
    seuil = 2
    wagon.position = segments[update_indice][1]
    update_suivant = segments[update_indice][1]
    update_précédent = segments[update_indice][0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
    # Changement de liaison glissière si nécessaire
        # passage au segment d’après
        if norme([wagon.position[0] - update_suivant[0], wagon.position[1] - update_suivant[1]]) < seuil and wagon.velocity[0] >= 0:
            space.remove(joint)
            joint = création_liaison(
                space, ligne, segments, wagon, p_to_i_gauche[update_suivant])
            space.add(joint)
            # update des paramètres
            update_indice += 1
            update_suivant = segments[update_indice][1]
            update_précédent = segments[update_indice][0]

        # passage au segment d’avant
        if norme([wagon.position[0] - update_précédent[0], wagon.position[1] - update_précédent[1]]) < seuil and wagon.velocity[0] <= 0:
            space.remove(joint)
            joint = création_liaison(
                space, ligne, segments, wagon, p_to_i_droite[update_précédent])
            space.add(joint)
            # update des paramètres
            update_indice -= 1
            update_suivant = segments[update_indice][1]
            update_précédent = segments[update_indice][0]

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        space.step(1/200.0)
        pygame.display.flip()
        clock.tick(200)


if __name__ == '__main__':
    main()
