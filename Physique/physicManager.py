"""
Class physicManager qui gère la physique Pymunk
-on peut process la sim physique
-on peut effectuer scénario standart
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random
from typing import List
from wagon import *
# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util


class physicManager(object):

    def __init__(self, width, height, gravity=980, fps=30) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, gravity)

        # Physics
        # Time step
        self._dt = 1.0 / fps
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()
        self.createWagon()

        # Execution control and time until the next ball spawns

    def createWagon(self):
        self.wagon = Wagon(self._space, 5, 50, 20, (300, 100))

    def __processPullingWagons(self):

        for wagon in self.wagons:
            pass
        # TODO

    def process(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        # Progress time forward
        for x in range(self._physics_steps_per_frame):
            self._space.step(self._dt)

        if self._process_events() == "QUIT":
            return False

        self._clear_screen()
        self._draw_objects()
        pygame.display.flip()
        # Delay fixed time between frames
        self._clock.tick(50)
        pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
        return True

    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (111.0, 600 - 280),
                           (407.0, 600 - 246), 0.0),
            pymunk.Segment(static_body, (407.0, 600 - 246),
                           (407.0, 600 - 343), 0.0),
        ]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "QUIT"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)
