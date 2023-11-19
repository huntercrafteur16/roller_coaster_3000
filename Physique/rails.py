# Montagnes Russes
from geomdl import BSpline
from geomdl import utilities
import pymunk.pygame_util
import pymunk
import pygame
import sys
import random

random.seed(1)  # make the simulation the same each time, easier to debug


class Rail():
    """
    Classe permettant le paramètrage et l'affichage de rails sous forme de spline dans pymunsk
    """
    curvePts: list[tuple]
    # liste des intervalles contenant les points [(0,5),(10,100)] ******___****************

    segments: list[pymunk.Segment]

    def __init__(self, degree=2) -> None:
        self.curvePts = []
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.05
        self.curve.degree = degree
        self.width = 1
        self.segments = []
        # liste des intervalles contenant les points [(0,5),(10,100)] ******___****************
        self.pullingPts_int = []

    def addPoint(self, point: tuple, isPulling: bool):
        self.curvePts.append(point)

    def _addFreeRail(self, c_deb, c_fin, space: pymunk.Space):
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = (125, 125, 125, 255)
        railseg.elasticity = 0
        railseg.collision_type = 0  # la collision d'un rail non tractant sera 0
        self.segments.append(railseg)

        space.add(railseg)

    def _addPullRail(self, c_deb, c_fin, space: pymunk.Space):
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = (255, 0, 0, 255)
        railseg.elasticity = 0
        railseg.collision_type = 1  # la collision d'un rail  tractant sera 1
        self.segments.append(railseg)
        space.add(railseg)

    def renderRail(self, space):
        self.curve.ctrlpts = self.curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts

        for i, p in enumerate(bspline[:-1]):
            if i < len(bspline)/2:
                self._addFreeRail(p, bspline[i+1], space)
            else:
                self._addPullRail(p, bspline[i+1], space)
