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
    curvePts = []
    pullingPts = []

    def __init__(self, degree=2) -> None:
        self.curve = BSpline.Curve(degree=degree)
        self.curve.delta = 0.05
        self.curve.degree = 2

    def addPoint(self, point: tuple, isPulling: bool):
        self.curvePts.append(point)

    def renderRail(self, space):
        self.curve.ctrlpts = self.curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        bspline = self.curve.evalpts
        for i, p in enumerate(bspline[:-1]):
            railseg = pymunk.Segment(
                space.static_body, p, bspline[i+1], 1)
            railseg.elasticity = 0
            if i < len(bspline)/2:
                railseg.color = (255, 0, 0, 255)
            space.add(railseg)


class Physique():
    def __init__(self, screen):
        self.draw_option = pymunk.pygame_util.DrawOptions(screen)
        self.space = None
        self.new()

    def new(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 200

    def add_rails(self, bspline):
        rails = pymunk.Body(body_type=pymunk.Body.STATIC)
        rails.position = (300, 300)
        for i, p in enumerate(bspline[:-1]):
            rail = pymunk.Segment(rails, p, bspline[i+1], 1)
            rail.elasticity = 0
        self.space.add(rails)

    def run(self):
        self.space.debug_draw(self.draw_option)
        self.space.step(0.01)


class Spline():
    def __init__(self, screen, degree=2):
        self.screen = screen
        self.degree = degree
        self.curve = BSpline.Curve()
        self.curve.degree = degree
        self.curvePts = []
        self.count = 0

    def draw(self, curvePts):
        self.curve.ctrlpts = curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        self.curvePts = self.curve.evalpts

    def set_degree(self, d):
        self.curve.degree = d
        self.degree = d

    def add_point(self, xy):
        self.curvePts.append(xy)

    def render(self):
        if self.count >= 2:
            pygame.draw.lines(
                self.screen, (100, 100, 100), 0, self.curvePts)
        for i, point in enumerate(self.curvePts):
            if i == 0:
                pygame.draw.circle(
                    self.screen, (0, 140, 200), point, 5)
            else:
                pygame.draw.circle(
                    self.screen, (140, 140, 140), point, 5)
        if self.count >= self.curve.degree + 1:
            pygame.draw.lines(self.screen, (255, 0, 0, 255), 0,
                              self.curvePts, width=5)


class Canvas():
    def __init__(self, screen):
        self.screen = screen
        self.curve = Spline(screen)
        self.physics = Physique(self.screen)
        self.curvePts = []
        self.count = 0
        self.selected = None
        self.move_point = False
        self.add_mode = 0

    def add_point(self, xy):
        self.curve.add_point(xy)

    def render(self):
        if self.count >= 2:
            pygame.draw.lines(
                self.screen, (100, 100, 100), 0, self.curvePts)
        for i, point in enumerate(self.curvePts):
            if i == 0:
                pygame.draw.circle(
                    self.screen, (0, 140, 200), point, 5)
            else:
                pygame.draw.circle(
                    self.screen, (140, 140, 140), point, 5)
        if self.count >= self.curve.degree + 1:
            pygame.draw.lines(self.screen, (255, 0, 0, 255), 0,
                              self.curvePts, width=5)

    def simulate(self):
        self.physics.run()


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
    canvas = Canvas(screen)

    def update():
        screen.fill(color=(255, 255, 255, 255))
        canvas.simulate()
        canvas.render()
        pygame.display.update()

    update()

    # Add points to the curve
    canvas.add_point((100, 100))
    canvas.add_point((200, 300))
    canvas.add_point((400, 200))
    canvas.render()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()
