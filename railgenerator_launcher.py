"""
Module permetant la création et sauvegarde dans un fichier d'un parcours
"""
import sys
import ctypes
import pygame
from GUI.rail_generator import Canvas

ctypes.windll.user32.SetProcessDPIAware()
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1920, 700))
    canvas = Canvas(screen)

    def update():
        """
        Met à jour l'affichage
        """
        screen.fill((200, 255, 255))
        canvas.render()
        pygame.display.update()

    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                canvas.select_left(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                canvas.select_right(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                canvas.move_point = False
            elif event.type == pygame.MOUSEMOTION:
                canvas.move(event.pos)
        update()
