"""Classe Wagon qui ajoute un wagon à un space pymunk """

from pymunk.vec2d import Vec2d
import pymunk
from Physique.classes_travail_wagon import Start_line, Poly
from Physique.classes_travail_wagon import Circle, PivotJoint, DampedSpring, GrooveJoint


class Wagon:

    """wagon(space, Mass, L, h, position_init) will create a wagon of mass M, lenght L,
       height h and starting position of the center of the body.Tension sets the force 
       of the spring.
       For a flat line, choose position_init = (x, y_line-50 )
       Example: wagon(space, 5, 100, 50, (300, 150)) will add a wagon to space"""

    def __init__(self, space: pymunk.Space, Mass: float, L: float, h: float, position_init: tuple,
                 tension_ressort=8000, loco=False, StartingLine=False):
        self.gravity = space.gravity
        assert L >= 20, 'la longueur minimale est 20'
        assert h <= L, 'la hauteur doit être inférieure à la largeur'
        self.is_loco = loco
        # repartition des masses
        if StartingLine:
            Start_line(space, (position_init[0]-(L/2+10)-50, position_init[1]+50),
                       (position_init[0]+L/2+10+50, position_init[1]+50))
        Mass_roues, Mass_chassis = (1/3)*Mass, (2/3)*Mass

        # Ajout des objets

        p = Vec2d(position_init[0], position_init[1])
        vs = [(-L/2, -h/2), (L/2, -h/2), (L/2, h/2),
              (-L/2, h/2), ((2*L/3), 0), ((-2*L/3), 0)]
        v2, v3 = vs[2], vs[3]
        v4 = (-L/2, h+L/6+3)
        v5 = (-L/2, h/2)
        v6 = (L/2, h+L/6+3)
        v7 = (+L/2, h/2)

        chassis = Poly(space, p, vs, Mass_chassis, L, h)

        wheel3 = Circle(space, p+v4, Mass_roues/4, 0, L/6)
        wheel4 = Circle(space, p+v6, Mass_roues/4, 0, L/6)
        if self.is_loco:
            wheel1 = Circle(space, p+v2, Mass_roues/4, 5, L/6)
            wheel2 = Circle(space, p+v3,  Mass_roues/4, 5, L/6)
        else:
            wheel1 = Circle(space, p+v2, Mass_roues/4, 4, L/6)
            wheel2 = Circle(space, p+v3,  Mass_roues/4, 4, L/6)

        # Ajout des liaisons

        PivotJoint(space, chassis.body, wheel1.body, v2, (0, 0), False)
        PivotJoint(space, chassis.body, wheel2.body, v3, (0, 0), False)

        DampedSpring(space, chassis.body, wheel3.body,
                     v5, (0, 0), L/6, tension_ressort, 60)

        DampedSpring(space, chassis.body, wheel4.body,
                     v7, (0, 0), L/6, tension_ressort, 60)

        GrooveJoint(space, chassis.body, wheel3.body,
                    (-L/2, h/2), (-L/2, h/2+100), (0, 0))
        GrooveJoint(space, chassis.body, wheel4.body,
                    (L/2, h/2), (L/2, h/2+100), (0, 0))

        # Ajout des attributs utiles

        self.w1 = wheel1.shape
        self.w2 = wheel2.shape
        self.w3 = wheel3.shape
        self.w4 = wheel4.shape
        self.c = chassis.body
        self.m = Mass
        self.L = L
        self.h = h
        self.tension = tension_ressort
        self.StartingLine = StartingLine

    # définitions des getters

    def get_all_wheels_shape(self):
        """renvoie les roues de self"""
        return (self.w1, self.w2, self.w3, self.w4)

    def get_chassis_body(self):
        """renvoie le chassis de self"""
        return self.c

    def get_chassis_velocity(self):
        """renvoie la vitesse de self"""
        return self.get_chassis_body(
        ).velocity.rotated(-self.get_chassis_body().angle)

    def get_kinetic(self):
        """renvoie l'energie cinétique de self"""
        return 0.5*self.m*(self.get_chassis_velocity()[0])**2

    def get_potential(self, ref_point=600):
        """renvoie l'energie potentielle de self"""
        return self.m*self.gravity[1]*(ref_point-self.c.position[1])*0.8

    def get_total_energy(self):
        """renvoie l'energie mécanique de self"""
        return (self.get_kinetic() + self.get_potential())

    def get_chassis_acceleration(self):
        """renvoie l'accélération de self"""
        return self.c.force/self.m

    def get_starting_position(self, pos_rail: tuple[float, float]):
        """renvoie la position à laquelle appeler le wagon en fonction de la position du rail"""
        return (pos_rail[0], pos_rail[1]-(self.L/3))

    def get_puissance(self):
        """renvoie la puissance lorsqu'il est tracté"""
        force = self.c.force
        vitesse = self.get_chassis_velocity()
        puissance = force.dot(vitesse)
        return puissance
