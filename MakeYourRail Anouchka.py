from geomdl import BSpline
from geomdl import utilities
from random import randint

import pymunk
import pymunk.pygame_util
import pygame
import sys


pygame.init()


class Config():
    def __init__(self):
        self.fill = (255, 255, 255)
        self.width = 2
        self.color = (255, 180, 0)
        self.dark = (0, 0, 0)
        self.bright = (0, 255, 0)
        self.brightdanger = (255, 0, 0)
        self.restrict = False
        self.restrict_zone = (160, 200, 560, 600)
        self.show_points = True
        self.edit_mode = True


cfg = Config()


class Rail():
    """
    Classe permettant le paramètrage et l'affichage de rails sous forme 
    de spline dans pymunk
    """
    curvePts = []
    pullingPts = []
    constantSpeedPts = []

    def __init__(self, degree=2) -> None:
        self.curve = BSpline.Curve(degree=int(degree))
        self.curve.delta = 0.05
        self.curve.degree = int(degree)

    def addPoint(self, point: tuple, desc: tuple):
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


class Spline():
    def __init__(self, screen, degree=2):
        self.screen = screen
        self.degree = int(degree)
        self.curve = BSpline.Curve(degree=self.degree)
        self.curvePts = []
        self.count = 0

    def draw(self, curvePts):
        self.curve.degree = self.degree  # Set the degree first
        self.curve.ctrlpts = curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        self.curvePts = self.curve.evalpts

    def set_degree(self, degree=2):
        self.curve.degree = degree
        self.degree = degree

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
        if self.count >= self.degree + 1:
            pygame.draw.lines(self.screen, (255, 0, 0, 255), 0,
                              self.curvePts, width=5)


class Canvas():
    def __init__(self, screen):
        self.screen = screen
        self.curve = Spline(screen)
        self.physics = Rail()
        self.ctrl_points = []
        self.count = 0
        self.selected = None
        self.move_point = False
        self.add_mode = 0

        self.add_button = (20, 460, 50, 20)
        self.del_button = (90, 460, 50, 20)
        self.sel_button = (160, 460, 50, 20)
        self.hide_button = (230, 460, 50, 20)

        self.edit_button = (20, 460, 50, 20)

    def add_point(self, xy):
        self.curve.curvePts.append(xy)
        self.count += 1

        if self.count >= self.curve.degree + 1:
            self.curve.draw(self.curve.curvePts)

    def button_render(self):
        if cfg.edit_mode:
            if self.add_mode:
                pygame.draw.rect(self.screen, cfg.bright, self.add_button)
            else:
                pygame.draw.rect(self.screen, cfg.dark, self.add_button)
            if self.selected != None:
                pygame.draw.rect(self.screen, cfg.bright, self.sel_button)
                pygame.draw.rect(
                    self.screen, cfg.brightdanger, self.del_button)
            pygame.draw.rect(self.screen, cfg.dark, self.hide_button)
        else:
            pygame.draw.rect(self.screen, cfg.dark, self.edit_button)

    def render(self):
        if cfg.edit_mode:
            if cfg.show_points:
                if self.count >= 2:
                    pygame.draw.lines(
                        self.screen, (100, 100, 100), 0, self.ctrl_points)
                    # cette ligne trace les segments entre les points
                for i, point in enumerate(self.ctrl_points):
                    if i == 0:
                        pygame.draw.circle(
                            self.screen, (0, 0, 200), point, 5)
                        # le premier point du tracé
                    elif i == self.selected:
                        pygame.draw.circle(
                            self.screen, (0, 200, 0), point, 5)
                        # le point séléctionné (pour le bouger)
                    else:
                        pygame.draw.circle(
                            self.screen, (140, 140, 140), point, 5)
                        # les autres points
            if self.count >= self.curve.degree+1:
                pygame.draw.lines(self.screen, cfg.color, 0,
                                  self.curve.curvePts, width=cfg.width)
                # la courbe calculée
        self.button_render()

    def region(self, button, x, y):
        bx, by, brx, bry = button
        if bx < x < bx+brx and by < y < by+bry:
            return True
        return False

    def select(self, x, y, r=10):
        if cfg.edit_mode:
            can_add = True
            if self.region(self.add_button, x, y):
                self.add_mode = not self.add_mode
                can_add = False
            elif self.region(self.sel_button, x, y):
                self.selected = None
                can_add = False

            elif self.region(self.hide_button, x, y):
                cfg.show_points = not cfg.show_points
                self.selected = None
                can_add = False

            elif self.region(self.del_button, x, y):
                if self.selected:
                    self.ctrl_points.pop(self.selected)
                    self.count -= 1
                    self.selected = None
                    can_add = False
                    if self.count >= self.curve.degree+1:
                        self.curve.draw(self.ctrl_points)
            elif self.count:
                for i, points in enumerate(self.ctrl_points):
                    px, py = points
                    if px-r < x < px+r and py-r < y < py+r:
                        self.selected = i
                        self.move_point = True
                        can_add = False
                        break
            if self.add_mode and can_add:
                self.count += 1
                if self.selected != None:
                    xpoint, _ = self.ctrl_points[self.selected]
                    if xpoint > x:
                        self.ctrl_points.insert(self.selected, (x, y))
                    else:
                        self.ctrl_points.insert(self.selected+1, (x, y))

                else:
                    self.ctrl_points.append((x, y))
                if self.count >= self.curve.degree+1:
                    self.curve.draw(self.ctrl_points)

        else:
            if self.region(self.edit_button, x, y):
                self.physics.new()
                cfg.edit_mode = True

    def move(self, xy):
        if self.move_point:
            self.ctrl_points.pop(self.selected)
            self.ctrl_points.insert(self.selected, xy)
            if self.count >= self.curve.degree+1:
                self.curve.draw(self.ctrl_points)

            return True


if __name__ == "__main__":
    screen = pygame.display.set_mode((500, 500))
    canvas = Canvas(screen)

    def update():
        screen.fill(cfg.fill)
        canvas.render()
        pygame.display.update()

    update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                canvas.select(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                canvas.move_point = False
            elif event.type == pygame.MOUSEMOTION:
                canvas.move(event.pos)
        update()
