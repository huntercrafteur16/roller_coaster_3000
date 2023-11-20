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

    - rails "FREE": collision_type = 0
    - rails "PROP": collision_type = 1
    - rails "PULL": collision_type = 2
    - rails "BRAKE": collision_type = 3 TODO actuellement c'est celui des wagons
    TODO modifier collision_type des wagons
    """
    curvePts: list[tuple[float, float, str]]
    # liste des intervalles contenant les points [(0,5),(10,100)] ******___****************

    segments: list[pymunk.Segment]

    def __init__(self, degree=2) -> None:
        self.curvePts = []
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.05
        self.curve.degree = degree
        self.width = 1
        self.segments = []
        self.pullingPts_int = []

    def addPoint(self, point: tuple, rail_type="FREE"):
        """Ajoute un point à l'objet rail choisi
        rail_type: "FREE","PULL","PROP","BRAKE"
        """
        p = (point[0], point[1], rail_type)
        self.curvePts.append(p)

    def _addFreeRail(self, c_deb, c_fin, space: pymunk.Space):
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = (125, 125, 125, 255)
        railseg.elasticity = 0
        railseg.collision_type = 0  # la collision d'un rail non tractant sera 0
        self.segments.append(railseg)

        space.add(railseg)

    def _addPropRail(self, c_deb, c_fin, space: pymunk.Space):
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = (255, 0, 0, 255)
        railseg.elasticity = 0
        railseg.collision_type = 1  # la collision d'un rail  tractant sera 1
        self.segments.append(railseg)
        space.add(railseg)

    def _addBrakeRail(self, c_deb, c_fin, space: pymunk.Space):
        pass

    def _addPullRail(self, c_deb, c_fin, space: pymunk.Space):
        pass

    def renderRail(self, space):
        """Permet d'ajouter le rail dans l'espace pymunk indiqué
        options: liste des coordonnées a_deb,a_fin et type du segment en question
        """

        self.curve.ctrlpts = [(x[0], x[1]) for x in self.curvePts]
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts
        if self.options is None:
            for i, p in enumerate(bspline[:-1]):
                if i < len(bspline)/2:
                    self._addFreeRail(p, bspline[i+1], space)
                else:
                    self._addPropRail(p, bspline[i+1], space)
        else:
            for i in self.options:
                if i[2] == "FREE":
                    self._addFreeRail(i[0], i[1], space)
                if i[2] == "PROP":
                    self._addPropRail(i[0], i[1], space)

                if i[2] == "PULL":
                    self._addPullRail(i[0], i[1], space)

                if i[2] == "BRAKE":
                    self._addBrakeRail(i[0], i[1], space)
