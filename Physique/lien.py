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


class Lien:
    def __init__(self, space, chassis_locomotive, chassis_wagon):
        L1 = chassis_locomotive.L
        L2 = chassis_wagon.L
        point_attache_loc = (-(4*L1/6), 0)
        point_attache_wag = ((4*L2/6), 0)
        PinJoint(space, chassis_locomotive, chassis_wagon,
                 point_attache_loc, point_attache_wag)
