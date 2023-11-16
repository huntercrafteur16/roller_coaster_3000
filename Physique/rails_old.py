# Montagnes Russes
from geomdl import BSpline
from geomdl import utilities
import pymunk.pygame_util
import pymunk
import pygame
import sys
import random

random.seed(1)  # make the simulation the same each time, easier to debug

'''
#Copier-coller aide d'internet
rails = BSpline.Curve()# Create a 3-dimensional B-spline Curve
rails.degree = 3# Set degree
rails.ctrlpts = [[10, 5, 10], [10, 20, -30], [40, 10, 25], [-10, 5, 0]]# Set control points
rails.knotvector = [0, 0, 0, 0, 1, 1, 1, 1]# Set knot vector
rails.delta = 0.05# Set evaluation delta (controls the number of curve points)
rails_points = rails.evalpts# Get curve points (the curve will be automatically evaluated)
'''

'''
Faire un rail qui peut
-ajouter des points à sa courbe
-générer le solide dans pymunk
-préciser les segments tractants et ceux non tractant

'''


class Rail():
    curvePts = []
    pullingPts = []

    def __init__(self, degree=2) -> None:
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.0

    def addPoint(self, point: tuple, isPuling: bool):
        self.curve.ctrlpts.append(point)
        if isPuling:
            self.pullingPts.append(point)

    def renderRail(self, space):
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts
        for i, p in enumerate(bspline[:-1]):
            railseg = pymunk.Segment(
                self.space.static_body, p, bspline[i+1], 1)
            railseg.elasticity = 0
            if p in self.pullingPts:
            
            space.add(railseg)


class Physique():
    def __init__(self, screen):
        self.draw_option = pymunk.pygame_util.DrawOptions(screen)
        self.space = None
        self.new()

    def new(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 200
    # creation d'un objet static + la courbe est decrite par la liste des points bspline
    # Question : comment definir bspline ?

    def add_rails(self, bspline):
        rails = pymunk.Body(body_type=pymunk.Body.STATIC)
        rails.position = (300, 300)
        for i, p in enumerate(bspline[:-1]):
            rails = pymunk.Segment(self.space.static_body, p, bspline[i+1], 1)
            rails.elasticity = 1
            self.space.add(rails)

    # Ajouter l'objet à l'espace
    def run(self):
        self.space.debug_draw(self.draw_option)
        self.space.step(0.01)


class Spline():
    def __init__(self, degree=2):
        self.degree = degree
        self.curve = BSpline.Curve()
        self.curve.degree = degree

        self.points = []

    def draw(self, points):
        self.curve.ctrlpts = points
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        # self.curve.vis = VisMPL.VisCurve3D()
        self.points = self.curve.evalpts

    def set_degree(self, d):
        self.curve.degree = d
        self.degree = d

    def add_points(self, xy):
        self.ctrl_points.append(xy)

    def render(self):
        if cfg.edit_mode:
            if cfg.show_points:
                if self.count >= 2:
                    pygame.draw.lines(
                        self.screen, (100, 100, 100), 0, self.ctrl_points)
                for i, point in enumerate(self.ctrl_points):
                    if i == 0:
                        pygame.draw.circle(
                            self.screen, (0, 140, 200), point, 5)
                    elif i == self.selected:
                        pygame.draw.circle(
                            self.screen, (20, 200, 80), point, 5)
                    else:
                        pygame.draw.circle(
                            self.screen, (140, 140, 140), point, 5)
            if self.count >= self.curve.degree+1:
                pygame.draw.lines(self.screen, cfg.color, 0,
                                  self.curve.points, width=cfg.width)
        self.button_render()


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
    canvas = Canvas(screen)

    def update():
        screen.fill(color="#444444")
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
