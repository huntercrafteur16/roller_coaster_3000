# Montagnes Russes
from geomdl import BSpline
from geomdl import utilities
import pymunk.pygame_util
import pymunk
import pygame
import sys
import random

random.seed(1)  # make the simulation the same each time, easier to debug


class Rail():
    """
    Classe permettant le paramètrage et l'affichage de rails sous forme 
    de spline dans pymunk
    """
    curvePts = []
    pullingPts = []
    constantSpeedPts = []

    def __init__(self, degree=2) -> None:
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.05
        self.curve.degree = degree

    def addPoint(self, point: tuple, desc: tuple):
        """
        Le tuple point décrit les coordonées du point dans l'espace
        Le tuple desc décrit le segment dont l'extrémité gauche est le point
        Ce tuple contient 2 booléens (les 2 ne peuvent pas être True)
        (le segement va accéléré le wagon,le segment donne une vitesse constante au wagon)
        """
        self.curvePts.append(point)

    def renderRail(self, space):
        """
        Cette fonction crée la courbe comme un objet de pymunk 
        donc affichable dans l'espace
        """
        self.curve.ctrlpts = self.curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts
        for i, p in enumerate(bspline[:-1]):
            railseg = pymunk.Segment(
                space.static_body, p, bspline[i+1], 1)
            railseg.elasticity = 0

            def constantSpeed_parts(bspline):
                """
                le but ici est de mettre en mouvement le wagon au début
                si celui-ci est en pente montante
                """
                def calculate_derivatives(bspline):
                    derivatives = []
                    for k in range(1, len(bspline)-1):
                        slope = (bspline[k+1]-bspline[k])/self.curve.delta
                        derivatives.append(slope)
                    return slope
                derivatives = calculate_derivatives(bspline)
                first_descendant_ind = 0
                while derivatives[k] >= 0:
                    k += 1
                first_descendant_ind = k
                if i < first_descendant_ind:
                    railseg.color = (255, 0, 0, 255)
                    constantSpeedPts.append(i)
                """
                le but ici est de faire choisir à l'utilisateur les parties à vitesse
                constantes (en plus de la partie pas défaut si elle existe)
                """
                for i in range(bspline):
                    if bspline[i].desc[1]:
                        railseg.color = (255, 0, 0, 255)
                        constantSpeedPts.append(i)
                return

            def pulling_parts(bspline):
                """
                Le but ici est de faire choisir à l'utilisateur des parties du circuit
                ou le wagon est accéléré par une force
                """
                for i in range(len(bspline)):
                    if bspline[i].desc[0]:
                        railseg.color = (0, 0, 255, 255)
                        pullingPts.append(i)
            constantSpeed_parts(bspline)
            pulling_parts(bspline)
            space.add(railseg)


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
    canvas = Canvas(screen)

    def update():
        screen.fill(color=(255, 255, 255, 255))
        canvas.simulate()
        canvas.render()
        pygame.display.update()

    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()
