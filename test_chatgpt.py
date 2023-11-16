import pymunk
import pygame
from pygame.locals import QUIT
import sys
import pymunk.pygame_util
# Initialisation de Pygame
pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Initialisation de l'espace Pymunk
space = pymunk.Space()
space.gravity = (0, 1000)  # Définir la gravité selon vos besoins

# Création du sol
ground = pymunk.Segment(space.static_body, (0, 200), (width, 200), 1)
ground.friction = 1.0
space.add(ground)

# Création de la liaison glissière
body = pymunk.Body()
body.position = (300, 200)
box = pymunk.Poly.create_box(body)
box.mass = 1
space.add(body, box)

pivot = pymunk.PivotJoint(space.static_body, body, body.position)
space.add(pivot)

slide = pymunk.SlideJoint(space.static_body, body,
                          (300, 200), (400, 200), 0, 50)
slide.collide_bodies = False
space.add(slide)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Mise à jour de l'espace Pymunk
    space.step(1 / 60.0)

    # Effacer l'écran
    screen.fill((255, 255, 255))

    # Dessiner les formes Pymunk
    space.debug_draw(draw_options)

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)
