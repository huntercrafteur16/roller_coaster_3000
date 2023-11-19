import sys
import pygame
from GUI.railGenerator import Canvas


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1000, 700))
    canvas = Canvas(screen)

    def update():
        screen.fill((255, 255, 255))
        canvas.render()
        pygame.display.update()

    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                canvas.select(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                canvas.move_point = False
            elif event.type == pygame.MOUSEMOTION:
                canvas.move(event.pos)
        update()
