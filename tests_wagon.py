import pymunk
import pymunk.pygame_util
from Physique.wagon import Wagon


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
