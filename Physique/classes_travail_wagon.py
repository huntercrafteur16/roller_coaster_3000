"""definit toutes les classes de travail qui permettent la
 contruction du wagon et du train"""

import pymunk
import numpy as np


class PivotJoint:
    """Classe PivotJoint : ajoute à space une liaison pivot entre le Body b et le body b2, 
    avec les points d'encrage a et a2 (coordonées locales), collide est un booléen 
    autorisant ou non les colisions."""

    def __init__(self, space: pymunk.Space, b: pymunk.body.Body,
                 b2: pymunk.body.Body, a=(0, 0), a2=(0, 0), collide=False):
        joint = pymunk.PinJoint(b, b2, a, a2)
        joint._set_error_bias(1e-6)
        joint.collide_bodies = collide
        space.add(joint)


class Segment:
    """Classe Segment : ajoute à space une ligne à partir du point p0 suivant le vecteur v, 
   d'épaisseur radius."""
    color = (0, 255, 0, 0)
    density = 0.1
    def __init__(self, space: pymunk.Space, p0: tuple[float, float],
                 v: tuple[float, float], radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = Segment.density
        shape.elasticity = 0
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = Segment.color
        self.shape = shape
        space.add(self.body, shape)


class Circle:
    """Classe Circle : ajoute à space un cercle à position, de masse Mass et de rayon radius"""

    def __init__(self, space: pymunk.Space, pos: tuple[float, float],
                 Mass: float, collision: float, radius=20.0):
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

    def __init__(self, space: pymunk.Space, p0=(0, 0), p1=(400, 200), d=4):
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

    def __init__(self, space: pymunk.Space, p0: tuple[float, float], p1: tuple[float, float]):
        segment = pymunk.Segment(space.static_body, p0, p1, 2)
        segment.elasticity = 1
        segment.friction = 1
        space.add(segment)


class Poly:
    """Classe Poly: ajoute à space un polynome à la position pos,
     avec les points vertices, de mass Mass si l'aire est L*h"""

    def __init__(self, space: pymunk.Space, pos: tuple[float, float], vertices: list,
                 Mass: float, L: float, h: float):
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
    """Classe Poly: ajoute à space un ressort entre body b et b2, 
     avec les ancrages anchor_b, anchor_b2 (coordonées locales),
     de longueur au repos rest_length, raideur stiffness controle damping"""

    def __init__(self, space: pymunk.Space, b: pymunk.body.Body, b2: pymunk.body.Body,
                 anchor_b: tuple[float, float], anchor_b2: tuple[float, float], rest_length: float,
                 stiffness: float, damping: float):
        joint = pymunk.DampedSpring(
            b, b2, anchor_b, anchor_b2, rest_length, stiffness, damping)
        space.add(joint)


class GrooveJoint:
    """Classe GrooveJoint: ajoute une liaison Groove entre a et b avec
      l'ancrage anchor_b sur b (coordonées locales),
      avec une glissière entre groove_a et groove_b"""

    def __init__(self, space: pymunk.Space, a: pymunk.body.Body, b: pymunk.body.Body,
                 groove_a: tuple[float, float], groove_b: tuple[float, float],
                 anchor_b: tuple[float, float]):
        joint = pymunk.GrooveJoint(
            a, b, groove_a, groove_b, anchor_b)
        joint.collide_bodies = False
        space.add(joint)


class PinJoint:
    """Classe PinJoint: ajoute une liaison entre a et b avec l'ancrage a
       sur b et a2 sur b2 (coordonées locales)"""

    def __init__(self, space: pymunk.Space, b: pymunk.body.Body, b2: pymunk.body.Body,
                 a=(0, 0), a2=(0, 0)):
        joint = pymunk.PinJoint(b, b2, a, a2)
        space.add(joint)
