from tkinter import GROOVE
from Physique.classes_travail_wagon import *
from pymunk.vec2d import Vec2d
import numpy as np
import pymunk
import sys
import pygame
import pymunk.pygame_util
import random
random.seed(1)


class Wagon:
    """wagon(space, Mass, L, h, position_init) will create a wagon of mass M, lenght L,

      height h and starting position of the center of the body.Tension sets the force of the spring.

        For a flat line, choose position_init = (x, y_line-50 )

        Example: wagon(space, 5, 100, 50, (300, 150)) will add a wagon to space"""

    def __init__(self, space, Mass: float, L: float, h: float, position_init: tuple, tension_ressort=500, StartingLine=False):

        assert L >= 20, 'la longueur minimale est 20'
        assert h <= L, 'la hauteur doit être inférieure à la largeur'

        # creation faculatative d'une ligne de départ sous le wagon
        if StartingLine:
            Start_line(space, (position_init[0]-(L/2+10)-50, position_init[1]+50),
                       (position_init[0]+L/2+10+50, position_init[1]+50))

        # repartition des masses

        Mass_roues, Mass_chassis = (1/3)*Mass, (2/3)*Mass

        # Ajout des objets

        p = Vec2d(position_init[0], position_init[1])
        vs = [(-L/2, -h/2), (L/2, -h/2), (L/2, h/2),
              (-L/2, h/2), ((4*L/6), 0), ((-4*L/6), 0)]
        v2, v3 = vs[2], vs[3]
        v4 = (-L/2, h+L)
        v5 = (-L/2, h/2)
        v6 = (L/2, h+L)
        v7 = (+L/2, h/2)

        chassis = Poly(space, p, vs, Mass_chassis, L, h)
        wheel1 = Circle(space, p+v2, Mass_roues/4, 2, L/6)
        wheel2 = Circle(space, p+v3,  Mass_roues/4, 2, L/6)
        wheel3 = Circle(space, p+v4, Mass_roues/4, 0, L/6)
        wheel4 = Circle(space, p+v6, Mass_roues/4, 0, L/6)

        # Ajout des liaisons

        PivotJoint(space, chassis.body, wheel1.body, v2, (0, 0), False)
        PivotJoint(space, chassis.body, wheel2.body, v3, (0, 0), False)

        DampedSpring(space, chassis.body, wheel3.body,
                     v5, (0, 0), L/6, tension_ressort, 60)

        DampedSpring(space, chassis.body, wheel4.body,
                     v7, (0, 0), L/6, tension_ressort, 60)

        GrooveJoint(space, chassis.body, wheel3.body,
                    (-L/2, h/2), (-L/2, h/2+100), (0, 0))
        GrooveJoint(space, chassis.body, wheel4.body,
                    (L/2, h/2), (L/2, h/2+100), (0, 0))

        # Ajout des attributs utiles

        self.w1 = wheel1.shape
        self.w2 = wheel2.shape
        self.w3 = wheel3.shape
        self.w4 = wheel4.shape
        self.c = chassis.body
        self.m = Mass
        self.L = L

    # définitions des getters

    def get_all_wheels_shape(self):
        return (self.w1, self.w2, self.w3, self.w4)

    def get_chassis_body(self):
        return (self.c)

    def get_chassis_velocity(self):
        return (self.c.velocity)

    def get_kinetic(self):
        return (self.c.kinetic_energy)

    def get_potential(self):
        return (self.m*9.81*(600-self.c.position[1]))

    def get_total_energy(self):
        return (self.get_kinetic() + self.get_potential())

    def get_chassis_acceleration(self):
        return (self.c.force/self.m)

    def get_starting_position(self, pos_rail: tuple):
        return ((pos_rail[0], pos_rail[1]-(self.L/4)))
