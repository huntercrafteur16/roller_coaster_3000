"""
Class physicManager qui gère la physique Pymunk
-on peut process la sim physique
-on peut effectuer scénario standart
"""
# Python imports
import os
import platform
from typing import Callable
import pymunk
import pymunk.pygame_util
import pygame
from Physique.wagon import Wagon
from Physique.rails import Rail
from Physique.ClasseTrain import *


class physicManager(object):
    """
    Manager du monde physique pymunk et de l'interaction entre les différentes actions
    """
    update_func: Callable  # fonction qui sera appelée à chaque boucle
    isPaused: bool
    time: int  # temps de la simulation en millisecondes

    def __init__(self, width, height, root=None, frame=None, gravity=980, fps=60) -> None:
        self.width = width
        self.height = height
        self.frame = frame
        self.gravity = gravity
        # code pour contenir la fenetre dans la frame tkinter indiquée #
        if frame is not None:
            os.environ['SDL_WINDOWID'] = str(frame.winfo_id())
            if platform.system() == "Windows":
                os.environ['SDL_VIDEODRIVER'] = 'windib'
        if root is not None:
            self.root = root

        # Réglage des paramètres temporels
        self._fps = fps
        self._dt = 1.0 / fps
        self._physics_steps_per_frame = 10

        # instanciation et réglage des paramètres physiques
        self._space = pymunk.Space()
        self._space.gravity = (0.0, gravity)

        # Number of physics steps per screen frame

        # initialisation de pygame avec paramètres
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._draw_options.constraint_color = (255, 255, 255, 255)
        self._draw_options.flags ^= pymunk.pygame_util.DrawOptions.DRAW_CONSTRAINTS

        # scénario test
        self.createTrain()
        self._createSampleRail()

        pygame.display.init()
        # réglages autres
        # fonction qui sera exécutée après chaque actualisation
        self.update_func = lambda: None
        self.isPaused = True
        self.time = 0
        self.pausedTime = 0

    def createTrain(self):  # va être bientôt supprimée servait pour le premier MVP

        self.wagon = Wagon(self._space, 5, 50, 30, (330, 130), 800)
        wagon_handler = self._space.add_collision_handler(2, 1)
        wagon_handler.pre_solve = self._onRailCollision
        self.Train = Train(self._space, self.wagon, 3)

    def getWagon(self):
        "retoure le wagon"
        return self.wagon

    def process(self) -> bool:
        """
        Boucle principale de la simulation qui permet d'actualiser la physique et l'affichage pygame
        :return: Bool selon que l'on doive continuer ou arrêter la boucle
        """
        # on court circuit le process si on pause le temps
        if self.isPaused:
            self._clock.tick_busy_loop(self._fps)
            return True

        # frames de simulation physique pour 1 frame d'affichage (physics oversampling)
        for _ in range(self._physics_steps_per_frame):
            self._space.step(self._dt/self._physics_steps_per_frame)

        if self._process_events() == "QUIT":  # vérification des évènements terminaux

            return False
        # fonctions nécessaires et explicites
        self._clear_screen()
        self._draw_objects()

        # fonction externe envoyée lors de l'exécution de process
        self.update_func()

        # actualisation du rendu pygame
        try:
            pygame.display.flip()
        except:
            pass

        # On pause la simulation selon les fps voulus
        self.time += self._clock.tick_busy_loop(self._fps)

        # pygame.display.set_caption("fps: " + str(self._clock.get_fps())) #affichage du nombre de fps sur le titre de la fenêtre
        return True  # aucun problème ni arrêt

    def _process_events(self) -> str:
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
                return "NOTHING"
        return "NOTHING"

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        try:
            self._screen.fill(pygame.Color("white"))

        except:
            pygame.init()
            pygame.display.init()
            print("error")

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)

    def _createSampleRail(self):
        self.rail = Rail()
        self.rail.addPoint((50, 200), False)
        self.rail.addPoint((250, 100), True)
        self.rail.addPoint((450, 300), True)
        self.rail.addPoint((600, 400), False)
        self.rail.addPoint((800, 400), False)
        self.rail.addPoint((1000, 300), False)

        self.rail.renderRail(self._space)

    def _pull_wagon(self, wagon: Wagon):
        wagon.get_chassis_body().apply_force_at_local_point((1000, 0), (0, 0))

    def _pull_body(self, body: pymunk.Body):
        body.apply_force_at_local_point((10000, 0), (0, 0))

    def _onRailCollision(self, arbiter, space, data):

        self._pull_body(arbiter.shapes[0].body)
        return True

    def getTime(self) -> int:
        """
        Renvoie le temps du programme en millisecondes
        """
        return self.time

    def pause(self) -> None:
        """Pause le temps de la simulation"""
        self.isPaused = True
        self.pausedTime = self.getTime()

    def play(self) -> None:
        """redémarre le temps de la simulation"""
        self.isPaused = False
        self.time = self.pausedTime

    def reinit(self):
        self._clear_screen()
        self._space = pymunk.Space()
        self.createTrain()
        self._createSampleRail()

        # réglages autres
        # fonction qui sera exécutée après chaque actualisation
        self.update_func = lambda: None
        self.isPaused = True
        self.time = 0
        self.pausedTime = 0
