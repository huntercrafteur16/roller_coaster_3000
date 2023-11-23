"""
fichier regroupant tout les tests
"""
import pygame
import pymunk
import pymunk.pygame_util
from GUI.graphiques import AnimatedGraph
from GUI.interface import Interface
from GUI.rail_generator import Config, Canvas
from GUI.resultInterface import ResultInterface
from Physique.wagon import Wagon
from Physique.classes_travail_wagon import Box, PinJoint, GrooveJoint, Poly, PivotJoint
from Physique.classes_travail_wagon import DampedSpring, Segment, Circle, Start_line
from Physique.physicManager import physicManager
from Physique.ClasseTrain import Train
from Physique.rails import Rail

### Tests###

space = pymunk.Space()
b1 = pymunk.Body(1)
b2 = pymunk.Body(2)
pivot = PivotJoint(space, b1, b2)
segment = Segment(space, (0, 0), (100, 0))
circle = Circle(space, (0, 0), 1, 1,)
start = Start_line(space, (0, 0), (100, 0))
box = Box(space, (0, 0), (400, 200))
poly = Poly(space, (0, 0), [(100, 0), (101, 0), (101, 1)], 1, 1, 1)
spring = DampedSpring(space, b1, b2, (0, 0), (0, 0), 10, 100, 1)
groove = GrooveJoint(space, b1, b2, (100, 200), (200, 300), (100, 100))
pinjoint = PinJoint(space, b1, b2, (0, 1))
x0, y0 = (0, 0)
x1, y1 = (400, 200)
pts = [(x0, y0), (x1, y0+20), (x1, y1+20), (x0, y1)]
assert pivot.collide is False
assert segment.body.position == (0, 0)
assert circle.body.position == (0, 0)
assert start.position == (0, 0)
assert box.points == pts
assert poly.vertices == [(100, 0), (101, 0), (101, 1)]
assert spring.stif == 100
assert groove.anchor_b == (100, 100)
assert pinjoint.a == (0, 1)


anim = AnimatedGraph('test')
assert isinstance(anim, AnimatedGraph)
assert not anim.t
assert not anim.data
assert anim._ymax == 0
assert anim._ymin == 0


manager = physicManager(1000, 600)
assert isinstance(manager, physicManager)


rail = Rail()
assert isinstance(rail, Rail)
assert not rail.data_points
rail.addPoint((0, 0))
assert rail.data_points == [(0, 0, 'FREE')]
rail._addPropRail((0, 0), (100, 0), space)
assert isinstance(rail.segments[0], pymunk.Segment)
rail._addFreeRail((0, 0), (100, 0), space)
assert isinstance(rail.segments[1], pymunk.Segment)
rail._addPullRail((0, 0), (100, 0), space)
assert isinstance(rail.segments[2], pymunk.Segment)
rail._addBrakeRail((0, 0), (100, 0), space)
assert isinstance(rail.segments[3], pymunk.Segment)


space = pymunk.Space()
wag = Wagon(space, 5, 40, 30, (300, 150))
train = Train(space, wag, 2)
assert isinstance(train.liste_wagon, list)
assert isinstance(train.liste_wagon[0], Wagon)
assert isinstance(train.liste_wagon[1], Wagon)
assert train.liste_wagon[0] == wag
assert train.liste_wagon[1].L == train.liste_wagon[0].L
assert train.liste_wagon[1].h == train.liste_wagon[0].h
assert train.liste_wagon[1].m == train.liste_wagon[0].m
assert len(train.liste_wagon) == 2


space = pymunk.Space()
wag = Wagon(space, 5, 40, 30, (300, 150))
assert isinstance(wag.w1, pymunk.shapes.Circle)
assert isinstance(wag.w2, pymunk.shapes.Circle)
assert isinstance(wag.w3, pymunk.shapes.Circle)
assert isinstance(wag.w4, pymunk.shapes.Circle)
assert isinstance(wag.c, pymunk.body.Body)
assert isinstance(wag.L, int)
assert wag.L == 40
assert isinstance(wag.h, int)
assert wag.h == 30
assert isinstance(wag.m, int)
assert wag.m == 5
assert wag.c.position == (300, 150)

d = {"show_results": 1, "open": 1, "apply": 1, "play_pause": 1, "start_reset": 1}
interface = Interface(d)
assert isinstance(interface, Interface)


config = Config()
assert isinstance(config, Config)
assert config.fill == (255, 255, 255)
assert config.width == 2
assert config.restrict is False
assert config.restrict_zone == (160, 200, 560, 600)
assert config.show_points is True
screen = pygame.Surface((0, 0))
canvas = Canvas(screen)
assert canvas.screen == screen
assert canvas.spline.degree == 2
assert canvas.spline.delta == 1e-3
assert not canvas.ctrl_points
assert not canvas.curve_points
assert not canvas.maindata
assert canvas.count == 0
assert canvas.selected is None
assert canvas.move_point is False
assert canvas.add_mode == 0
assert not canvas.lineselection


result = ResultInterface(1, 'test')
assert isinstance(result, ResultInterface)
assert result.subplt_nbr == 1
assert result.subplt_titles == 'test'
