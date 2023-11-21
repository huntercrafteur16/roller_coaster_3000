import sys
import pygame
from GUI.railGenerator import Canvas


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1200, 600))
    canvas = Canvas(screen)

    def update():
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
