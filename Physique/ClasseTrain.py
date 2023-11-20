from Physique.wagon import *
from Physique.classes_travail_wagon import *
import random
random.seed(1)


class Lien:
    """Crée le lien entre la locomotive et le wagon données en paramètres"""

    def __init__(self, space, locomotive: Wagon, wagon: Wagon):
        L1 = locomotive.L
        L2 = wagon.L
        point_attache_loc = (-(2*L1/3), 0)
        point_attache_wag = ((2*L2/3), 0)
        PinJoint(space, locomotive.c, wagon.c,
                 point_attache_loc, point_attache_wag)


class Train:
    def __init__(self, space, wagon: Wagon, nb_wagon: int):
        self.liste_wagon = [wagon]
        for i in range(1, nb_wagon):
            self.liste_wagon.append(Wagon(space, wagon.m, wagon.L, wagon.h, (
                self.liste_wagon[i-1].c.position[0]-(4*(wagon.L)/3)-(wagon.L/3), wagon.c.position[1]), wagon.tension, wagon.StartingLine))
            Lien(space, self.liste_wagon[i-1], self.liste_wagon[i])
