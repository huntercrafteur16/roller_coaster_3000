# Python imports
import random
from typing import List
from wagon import *

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util

# local import
from wagon import *


space = pymunk.Space()
wag = Wagon(space, 5, 40, 30, (300, 150))

assert type(wag.w1) == pymunk.shapes.Circle
assert type(wag.w2) == pymunk.shapes.Circle
assert type(wag.w3) == pymunk.shapes.Circle
assert type(wag.c) == pymunk.body.Body
