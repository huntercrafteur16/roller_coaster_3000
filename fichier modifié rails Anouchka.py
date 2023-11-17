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
    curvePts = []
    pullingPts = []

    def __init__(self, degree=2) -> None:
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.05
        self.curve.degree = degree

    def addPoint(self, point: tuple, isPulling: bool):
        self.curvePts.append(point)

    def renderRail(self, space):
        self.curve.ctrlpts = self.curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts
        for i, p in enumerate(bspline[:-1]):
            railseg = pymunk.Segment(
                space.static_body, p, bspline[i+1], 1)
            railseg.elasticity = 0
            def calculate_derivatives(bspline):
                derivatives=[]
                for k in range(1,len(bspline)-1):
                    slope=(bspline[k+1]-bspline[k])/self.curve.delta
                    derivatives.append(slope)
                return slope
            derivatives=calculate_derivatives(bspline)
            first_descendant_ind=0
            while derivatives[k]>=0:
                k+=1
            first_descendant_ind=k
            if i< first descendant_ind :
                railseg.color = (255, 0, 0, 255)
            space.add(railseg)


