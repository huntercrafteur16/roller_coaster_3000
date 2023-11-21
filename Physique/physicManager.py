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
import numpy as np
from Physique.wagon import Wagon
from Physique.rails import Rail
from Physique.ClasseTrain import Train


class physicManager(object):
    """
    Manager du monde physique pymunk et de l'interaction entre les différentes actions
    """
    update_func: Callable  # fonction qui sera appelée à chaque boucle
    isPaused: bool
    time: int  # temps de la simulation en millisecondes
    wagon_height = 10
    wagon_length = 20

    def __init__(self, width, height, root=None, frame=None, gravity=980, fps=60) -> None:
        self.width = width
        self.height = height
        self.frame = frame
        self.gravity = gravity
        self.rail = None  # type: ignore

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
        self._physics_steps_per_frame = 100

        # instanciation et réglage des paramètres physiques

        # Number of physics steps per screen frame

        # initialisation de pygame avec paramètres
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._draw_options.constraint_color = (255, 255, 255, 255)
        self._draw_options.flags ^= pymunk.pygame_util.DrawOptions.DRAW_CONSTRAINTS

        # scénario test
        pygame.display.init()
        # réglages autres
        # fonction qui sera exécutée après chaque actualisation
        self.update_func = lambda: None
        self.isPaused = True
        self.time = 0
        self.pausedTime = 0
        self.reinit()

    def createTrain(self, startpos: tuple[float, float], mass=5):
        """
        Crée le premier wagon et le reste du train
        """
        l = physicManager.wagon_length
        h = physicManager.wagon_height
        self.wagon = Wagon(self._space, mass, l, h, startpos, 8000, True)
        wagon_handler_prop = self._space.add_collision_handler(4, 1)
        wagon_handler_prop.pre_solve = self._on_prop_rail_Collision

        wagon_handler_prop = self._space.add_collision_handler(5, 1)
        wagon_handler_prop.pre_solve = self._on_prop_rail_Collision

        wagon_handler_pull = self._space.add_collision_handler(5, 2)
        wagon_handler_pull.pre_solve = self._on_pull_rail_Collision

        wagon_handler_brake = self._space.add_collision_handler(4, 3)
        wagon_handler_brake.pre_solve = self._on_brake_rail_Collision

        wagon_handler_brake = self._space.add_collision_handler(5, 3)
        wagon_handler_brake.pre_solve = self._on_brake_rail_Collision

        wagon_handler_drag = self._space.add_collision_handler(4, 0)
        wagon_handler_drag.pre_solve = self._on_drag_rail_Collision
        self.Train = Train(self._space, self.wagon, self.N)

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
            self._clear_screen()
            self._draw_objects()

        # fonction externe envoyée lors de l'exécution de process
            self.update_func()

        # actualisation du rendu pygame

            pygame.display.flip()
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

        pygame.display.flip()

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

    def _prop_loco(self, force):
        """exerce la force de traction sur la locomotive"""

        self.wagon.get_chassis_body().apply_force_at_local_point((force, 0))
        # body.apply_force_at_local_point((force, 0), (0, 0))

    def _pull_loco(self, speed_cons, K=3000):
        """exerce la force de traction sur la locomotive"""
        cur_speed = self.wagon.get_chassis_body(
        ).velocity.rotated(-self.wagon.get_chassis_body().angle)

        self._prop_loco((speed_cons-cur_speed[0])*K)

    def _on_brake_rail_Collision(self, arbiter, space, data):

        self._pull_loco(0, 200)
        return True

    def _on_drag_rail_Collision(self, arbiter, space, data):
        coef = 0.001
        vitesse = self.wagon.get_chassis_velocity()[0]
        signe = np.sign(vitesse)
        force = -signe*coef*vitesse**2
        self._prop_loco(force)
        return (True)

    def _on_prop_rail_Collision(self, arbiter, space, data):
        self._prop_loco(6000)
        return True

    def _on_pull_rail_Collision(self, arbiter, space, data):
        self._pull_loco(200)
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

    def reinit(self, param=None):
        """reinitialise la simulation"""
        # self._createSampleRail()

        self._space = pymunk.Space()
        self._space.gravity = (0.0, self.gravity)

        if self.rail:
            startpos = (self.rail.data_points[0]
                        [0], self.rail.data_points[0][1]-10)
            if param is not None:
                self.N = param["nbr_wagon"]
            self.rail.renderRail(
                self._space, physicManager.wagon_length, self.N)
        else:
            startpos = (self.width/2, self.height/2)

        if param is None:
            self.N = 3
            self.createTrain(startpos)
        else:

            self.createTrain(startpos, param["mass"])

        self.process()
        # self._createSampleRail()

        # réglages autres
        # fonction qui sera exécutée après chaque actualisation
        self.update_func = lambda: None
        self.isPaused = True
        self.time = 0
        self.pausedTime = 0
        self._screen.fill(pygame.Color("white"))

    def import_rails_from_file(self, chemin: str):
        """crée un rail à partir d'un fichier"""
        L = physicManager.wagon_length
        file = open(chemin, "r")
        lines = file.readlines()
        file.close()
        self.rail = Rail()
        for line in lines:
            L_point = line.split(',')
            point = (float(L_point[0]), float(L_point[1]))
            self.rail.addPoint(point, L_point[2].strip())
        self.rail.renderRail(self._space, L, self.N)

    def get_length_from_pixel(self, pixel, ratio):
        'ratio est le nombre de pixel pour un mètre'
        return pixel/ratio

    def get_pixel_from_length(self, length, ratio):
        'ratio est le nombre de pixel pour un nombre'
        return length*ratio
