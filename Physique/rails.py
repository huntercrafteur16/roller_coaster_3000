"""Module qui définit les classes relatives aux rails"""

import random
import pymunk.pygame_util
import pymunk


random.seed(1)  # make the simulation the same each time, easier to debug


class Rail():
    """
    Classe permettant le paramètrage et l'affichage de rails sous forme de spline dans pymunsk

    - rails "FREE": collision_type = 0
    - rails "PROP": collision_type = 1
    - rails "PULL": collision_type = 2
    - rails "BRAKE": collision_type = 3 
    """

    segments: list[pymunk.Segment]
    # coordonnés des points et type de liaison
    data_points: list[tuple[int, int, str]]
    color_free_rail = (60, 60, 60, 255)
    color_pull_rail = (250, 150, 0, 255)
    color_prop_rail = (220, 220, 0, 255)
    color_brake_rail = (250, 0, 0, 255)

    def __init__(self) -> None:
        self.data_points = []  # courbe qui sera lue du fichier enregistré
        self.width = 1
        self.segments = []

    def addPoint(self, point: tuple, rail_type="FREE"):
        """Ajoute un point à l'objet rail choisi
        rail_type: "FREE","PULL","PROP","BRAKE"
        """
        p = (point[0], point[1], rail_type)
        self.data_points.append(p)

    def _addFreeRail(self, c_deb, c_fin, space: pymunk.Space):
        """ajoute un segment de rail type FREE"""
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = Rail.color_free_rail
        railseg.elasticity = 0
        railseg.friction = 1
        railseg.collision_type = 0  # la collision d'un rail non tractant sera 0
        self.segments.append(railseg)

        space.add(railseg)

    def _addPropRail(self, c_deb, c_fin, space: pymunk.Space):
        """ajoute un segment de rail type PROP"""
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = Rail.color_prop_rail
        railseg.elasticity = 0
        railseg.friction = 1
        railseg.collision_type = 1  # la collision d'un rail prop sera 1
        self.segments.append(railseg)
        space.add(railseg)

    def _addBrakeRail(self, c_deb, c_fin, space: pymunk.Space):
        """ajoute un segment de rail type BRAKE"""
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = Rail.color_brake_rail
        railseg.elasticity = 0
        railseg.friction = 1
        railseg.collision_type = 3  # la collision d'un rail brake sera 3
        self.segments.append(railseg)
        space.add(railseg)

    def _addPullRail(self, c_deb, c_fin, space: pymunk.Space):
        """ajoute un segment de rail type PULL"""
        railseg = pymunk.Segment(space.static_body, c_deb, c_fin, self.width)
        railseg.color = Rail.color_pull_rail
        railseg.elasticity = 0
        railseg.friction = 1
        railseg.collision_type = 2  # la collision d'un rail  tractant sera 2
        self.segments.append(railseg)
        space.add(railseg)

    def add_premier_rail(self, space, L, nb_wagon):
        """ajoute le premier rail, qui permet de poser le train"""
        premier_point = (self.data_points[0][0], self.data_points[0][1])
        railseg = pymunk.Segment(space.static_body, premier_point, (
            premier_point[0]-2*L*nb_wagon, premier_point[1]), self.width)
        railseg.elasticity = 0
        railseg.collision_type = 2
        railseg.friction = 1
        space.add(railseg)

    def add_last_rail(self, space, L, nb_wagon):
        """ajoute le dernier rail, qui permet de poser le train"""
        dernier_point = (self.data_points[-1][0], self.data_points[-1][1])
        railseg = pymunk.Segment(space.static_body, dernier_point, (
            dernier_point[0]+4*L*nb_wagon, dernier_point[1]), self.width)
        railseg.elasticity = 0
        railseg.collision_type = 3
        railseg.friction = 1
        space.add(railseg)

    def renderRail(self, space, L, nb_wagon):
        """Permet d'ajouter le rail dans l'espace pymunk indiqué
        options: liste des coordonnées a_deb,a_fin et type du segment en question
        """

        # self.curve.ctrlpts = [(x[0], x[1]) for x in self.curvePts]
        # self.curve.knotvector = utilities.generate_knot_vector(
        #     self.curve.degree, len(self.curve.ctrlpts))
        # bspline = self.curve.evalpts
        self.add_premier_rail(space, L, nb_wagon)
        self.add_last_rail(space, L, nb_wagon)
        for i, p in enumerate(self.data_points[:-1]):

            if p[2] == "FREE":

                self._addFreeRail(
                    self.data_points[i][:2], self.data_points[i+1][:2], space)
            if p[2] == "PROP":
                self._addPropRail(
                    self.data_points[i][:2], self.data_points[i+1][:2], space)

            if p[2] == "PULL":
                self._addPullRail(
                    self.data_points[i][:2], self.data_points[i+1][:2], space)

            if p[2] == "BRAKE":
                self._addBrakeRail(
                    self.data_points[i][:2], self.data_points[i+1][:2], space)
