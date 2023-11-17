"""
Class physicManager qui gère la physique Pymunk
-on peut process la sim physique
-on peut effectuer scénario standart
"""
# Python imports
import random
from typing import List
from wagon import *
# Library imports
import pygame
from rails import *
# pymunk imports
import pymunk
import pymunk.pygame_util


class physicManager(object):

    def __init__(self, width, height, gravity=980, fps=30) -> None:
        # Space
        self._fps = fps
        self._space = pymunk.Space()
        self._space.gravity = (0.0, gravity)

        # Physics
        # Time step
        self._dt = 1.0 / fps
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 10

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self.createWagon()
        self._createSampleRail()

        # Execution control and time until the next ball spawns

    def createWagon(self):
        self.wagon = Wagon(self._space, 5, 150, 50, (300, 100), 800)

    def __processPullingWagons(self):

        for wagon in self.wagons:
            pass
        # TODO

    def process(self) -> None:
        """
        The main loop of the simulation.
        :return: None
        """
        # Main loop
        # Progress time forward
        # oversampling physics compared to fps
        for x in range(self._physics_steps_per_frame):
            self._space.step(self._dt/self._physics_steps_per_frame)

        if self._process_events() == "QUIT":
            return False

        self._clear_screen()
        self._draw_objects()
        pygame.display.flip()

        # Delay fixed time between frames
        self._clock.tick(self._fps)

        pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
        return True

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._pull_wagon(self.wagon)

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

    def _createSampleRail(self):
        rail = Rail()
        rail.addPoint((50, 200), False)
        rail.addPoint((250, 100), True)
        rail.addPoint((450, 300), True)
        rail.addPoint((600, 400), False)
        rail.addPoint((800, 400), False)
        rail.addPoint((1000, 300), False)

        rail.renderRail(self._space)

    def _pull_wagon(self, wagon: Wagon):
        wagon.get_chassis_body().apply_force_at_local_point((100000, 0), (0, 0))

    def onUpdate(self, func):
        func()
