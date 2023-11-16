# Python imports
import random
from typing import List
from wagon import *

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util

#local import
from wagon import *



space = pymunk.Space() 
wag = wagon(space,5, 40,30,(300,150))
assert type(wag.wheel1) = 