"""Classe train qui ajoute un train a un space pymunk et classe
 lien qui permet la construction de la classe train """


from Physique.wagon import Wagon
from Physique.classes_travail_wagon import PinJoint


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

    """Crée un train de nb_wagon wagons à partir d'un modèle de wagon donné. 
    Les wagon sont stockés dans une liste et le premier wagon de ce train est le wagon donné"""

    def __init__(self, space, wagon: Wagon, nb_wagon: int):
        self.liste_wagon = [wagon]
        for i in range(1, nb_wagon):
            self.liste_wagon.append(Wagon(space, wagon.m, wagon.L, wagon.h, (
                self.liste_wagon[i-1].c.position[0] -
                (4*(wagon.L)/3)-(wagon.L*(2/3)),
                wagon.c.position[1]), wagon.tension, wagon.StartingLine))
            Lien(space, self.liste_wagon[i-1], self.liste_wagon[i])
