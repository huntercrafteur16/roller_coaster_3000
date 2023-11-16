import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import numpy as np
import pygame
from pygame.locals import *
import math
from PIL import Image


class PivotJoint:
    def __init__(self, space, b, b2, a=(0, 0), a2=(0, 0), collide=True):
        joint = pymunk.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        space.add(joint)


class Segment:
    def __init__(self, space, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)


class Circle:
    def __init__(self, space, pos, Mass, radius=20):
        self.body = pymunk.Body()
        self.body.position = pos
        shape = pymunk.Circle(self.body, radius)
        shape.density = Mass/(np.pi*(radius**2))
        shape.friction = 1
        shape.elasticity = 0.1
        space.add(self.body, shape)


class Box:
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
    def __init__(self, space, p0, p1):
        x0, y0 = p0
        x1, y1 = p1
        segment = pymunk.Segment(space.static_body, p0, p1, 2)
        segment.elasticity = 1
        segment.friction = 1
        space.add(segment)


class Poly:
    def __init__(self, space, pos, vertices, Mass, L, h):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos
        shape = pymunk.Poly(self.body, vertices)
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.density = Mass/(L*h)
        shape.elasticity = 0.5
        shape.color = (255, 0, 0, 0)
        space.add(self.body, shape)


class DampedSpring:
    def __init__(self, space, b, b2, anchor_b, anchor_b2, rest_length, stiffness, damping):
        joint = pymunk.DampedSpring(
            b, b2, anchor_b, anchor_b2, rest_length, stiffness, damping)
        space.add(joint)
