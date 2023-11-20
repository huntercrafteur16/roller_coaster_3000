import pymunk
from Physique.wagon import Wagon
from Physique.ClasseTrain import Train

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
