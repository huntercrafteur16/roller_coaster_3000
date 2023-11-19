import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import numpy as np
import pygame
from pygame.locals import *
import math
from PIL import Image


class PivotJoint:
    """Classe PivotJoint : ajoute à space une liaison pivot entre le Body b et le body b2, 
    avec les points d'encrage a et a2 (coordonées locales), collide est un booléen 
    autorisant ou non les colisions."""

    def __init__(self, space, b, b2, a=(0, 0), a2=(0, 0), collide=False):
        joint = pymunk.PinJoint(b, b2, a, a2)
        joint._set_error_bias(1e-6)
        joint.collide_bodies = collide
        space.add(joint)


class Segment:
    """Classe Segment : ajoute à space une ligne à partir du point p0 suivant le vecteur v, 
   d'épaisseur radius."""

    def __init__(self, space, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        self.shape = shape
        space.add(self.body, shape)


class Circle:
    """Classe Circle : ajoute à space un cercle à position, de masse Mass et de rayon radius"""

    def __init__(self, space, pos, Mass, collision, radius=20):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos
        shape = pymunk.Circle(self.body, radius)
        shape.density = Mass/(np.pi*(radius**2))
        shape.collision_type = collision  # colision type of wheel
        shape.friction = 1
        shape.elasticity = 0.1
        shape.color = (175, 175, 175, 0)
        shape.shape_outline_color = (0, 0, 0, 0)
        self.shape = shape
        space.add(self.body, shape)


class Box:
    """Classe Box: ajoute à space une boite rectangulaire entre p0 et p1"""

    def __init__(self, space, p0=(0, 0), p1=(400, 200), d=4):
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0+20), (x1, y1+20), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(
                space.static_body, pts[i], pts[(i+1) % 4], d)
            segment.elasticity = 1
            segment.friction = 0.5
            space.add(segment)


class Start_line:
    """Classe Start_line: ajoute à space une ligne entre p0 et p1"""

    def __init__(self, space, p0, p1):
        x0, y0 = p0
        x1, y1 = p1
        segment = pymunk.Segment(space.static_body, p0, p1, 2)
        segment.elasticity = 1
        segment.friction = 1
        space.add(segment)


class Poly:
    """Classe Poly: ajoute à space un polynome à la position pos,
     avec les points vertices, de mass Mass si l'aire est L*h"""

    def __init__(self, space, pos, vertices, Mass, L, h):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos
        shape = pymunk.Poly(self.body, vertices)
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.density = Mass/(L*h)
        shape.elasticity = 0.5
        shape.color = (82.3, 70.1, 30.9, 0)

        self.shape = shape
        space.add(self.body, shape)


class DampedSpring:
    """Classe Poly: ajoute à space un ressort entre body b et b2, avec les ancrages anchor_b, anchor_b2 (coordonées locales),
     de longueur au repos rest_length, raideur stiffness controle damping"""

    def __init__(self, space, b, b2, anchor_b, anchor_b2, rest_length, stiffness, damping):
        joint = pymunk.DampedSpring(
            b, b2, anchor_b, anchor_b2, rest_length, stiffness, damping)
        space.add(joint)


class GrooveJoint:
    """Classe GrooveJoint: ajoute une liaison Groove entre a et b avec l'ancrage anchor_b sur b (coordonées locales),
     avec une glissière entre groove_a et groove_b"""

    def __init__(self, space, a, b, groove_a, groove_b, anchor_b):
        joint = pymunk.GrooveJoint(
            a, b, groove_a, groove_b, anchor_b)
        joint.collide_bodies = False
        space.add(joint)
