from geomdl import BSpline
from geomdl import utilities


import pygame
from Physique.rails import Rail


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


'''
class RailGenerator():
    """
    Classe permettant le paramètrage et l'affichage de rails sous forme 
    de spline dans pymunk
    """

    def __init__(self, screen, degree: int = 2) -> None:
        curvePts = []
        pullingPts = []
        constantSpeedPts = []
        self.screen = screen
        self.degree = degree
        self.curve = BSpline.Curve(degree=int(degree))
        self.curve.delta = 1e-3
        self.curve.degree = int(degree)
        self.count = 0

    def addPoint(self, point: tuple):
        self.curvePts.append(point)

    def set_degree(self, degree=2):
        self.curve.degree = degree
        self.degree = degree

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

    def draw(self, curvePts):
        self.curve.degree = self.degree  # Set the degree first
        self.curve.ctrlpts = curvePts
        self.curve.knotvector = utilities.generate_knot_vector(
            self.curve.degree, len(self.curve.ctrlpts))
        self.curvePts = self.curve.evalpts

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
    '''


class Canvas():
    """
    Classe d'affichage et de création d'un objet rail pour physic manager
    """
    rail_type_list = ["PROP", "PULL", "BRAKE", "FREE"]

    def __init__(self, screen: pygame.Surface):
        self.cfg = Config()
        self.screen = screen
        self.curve = Rail()
        # self.physics = Rail()
        self.ctrl_points = []
        self.count = 0
        self.selected = None
        self.move_point = False
        self.add_mode = 0
        self.rail_type = None
        # affichage graphique
        self.my_font = pygame.font.SysFont('Comic Sans MS', 10)
        width, height = screen.get_width(), screen.get_height()
        dh = 20
        dl = 50
        self.add_button = (width/8, height - 50, dl, dh)
        self.del_button = (2*width/8, height - 50, dl, dh)
        self.sel_button = (3*width/8, height - 50, dl, dh)
        self.hide_button = (4*width/8, height - 50, dl, dh)
        self.edit_button = (5*width/8, height - 50, 50, 20)
        self.confirm_button = (6*width/8, height - 50, 50, 20)
        self.free_type_button = ((7*width/8, height - 200, 50, 20))
        self.pull_type_button = ((7*width/8, height - 150, 50, 20))
        self.prop_type_button = ((7*width/8, height - 100, 50, 20))
        self.brake_type_button = ((7*width/8, height - 50, 50, 20))

    def button_render(self):
        if self.cfg.edit_mode:
            if self.add_mode:
                pygame.draw.rect(self.screen, self.cfg.bright, self.add_button)
                text_surface = self.my_font.render(
                    'ajout de points', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.add_button[0], self.add_button[1]+20))
            else:
                pygame.draw.rect(self.screen, self.cfg.dark, self.add_button)
                text_surface = self.my_font.render(
                    'ajouter un point', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.add_button[0], self.add_button[1]+20))
            if self.selected != None:

                pygame.draw.rect(self.screen, self.cfg.bright, self.sel_button)
                text_surface = self.my_font.render(
                    'déselectionner', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.sel_button[0], self.sel_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright, self.del_button)
                text_surface = self.my_font.render(
                    'supprimer', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.del_button[0], self.del_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright if self.rail_type == "FREE" else self.cfg.bright, self.free_type_button)
                text_surface = self.my_font.render(
                    'libre', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.free_type_button[0], self.free_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright if self.rail_type == "BRAKE" else self.cfg.bright, self.brake_type_button)
                text_surface = self.my_font.render(
                    'frein', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.brake_type_button[0], self.brake_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright if self.rail_type == "PULL" else self.cfg.bright, self.pull_type_button)
                text_surface = self.my_font.render(
                    'treuil', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.pull_type_button[0], self.pull_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright if self.rail_type == "PROP" else self.cfg.bright, self.prop_type_button)
                text_surface = self.my_font.render(
                    'entraîner', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.prop_type_button[0], self.prop_type_button[1]+20))

            pygame.draw.rect(self.screen, self.cfg.dark, self.hide_button)
            text_surface = self.my_font.render(
                'montrer/cacher', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.hide_button[0], self.hide_button[1]+20))
            pygame.draw.rect(self.screen, self.cfg.dark, self.confirm_button)
            text_surface = self.my_font.render(
                'valider', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.confirm_button[0], self.confirm_button[1]+20))
        else:
            pygame.draw.rect(self.screen, self.cfg.dark, self.edit_button)

    def render(self):
        if self.cfg.edit_mode:
            if self.cfg.show_points:
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
            if self.count >= self.curve.curve.degree+1:
                pygame.draw.lines(self.screen, self.cfg.color, 0,
                                  self.curve.curvePts, width=self.cfg.width)
                # la courbe calculée
        self.button_render()

    def region(self, button, x, y):
        bx, by, brx, bry = button
        if bx < x < bx+brx and by < y < by+bry:
            return True
        return False

    def select(self, x, y, r=10):
        if self.cfg.edit_mode:
            can_add = True
            if self.region(self.add_button, x, y):
                self.add_mode = not self.add_mode
                can_add = False
            elif self.region(self.sel_button, x, y):
                self.selected = None
                can_add = False

            elif self.region(self.hide_button, x, y):
                self.cfg.show_points = not self.cfg.show_points
                self.selected = None
                can_add = False

            elif self.region(self.del_button, x, y):
                if self.selected:
                    self.ctrl_points.pop(self.selected)
                    self.count -= 1
                    self.selected = None
                    can_add = False
                    if self.count >= self.curve.curve.degree+1:
                        self.draw(self.ctrl_points)
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
                if self.count >= self.curve.curve.degree+1:
                    self.draw(self.ctrl_points)

            if self.selected is not None:
                if self.region(self.free_type_button, x, y):
                    self.rail_type = "FREE"
                elif self.region(self.brake_type_button, x, y):
                    self.rail_type = "BRAKE"
                elif self.region(self.prop_type_button, x, y):
                    self.rail_type = "PROP"
                elif self.region(self.pull_type_button, x, y):
                    self.rail_type = "PULL"
            else:
                self.rail_type = None
        else:
            if self.region(self.edit_button, x, y):
                # self.physics = Rail()
                self.cfg.edit_mode = True

    def move(self, xy):
        if self.move_point:
            self.ctrl_points.pop(self.selected)
            self.ctrl_points.insert(self.selected, xy)
            if self.count >= self.curve.curve.degree+1:
                self.draw(self.ctrl_points)

            return True

    def draw(self, curvePts):
        self.curve.curve.degree = self.curve.curve.degree  # Set the degree first
        self.curve.curve.ctrlpts = curvePts
        self.curve.curve.knotvector = utilities.generate_knot_vector(
            self.curve.curve.degree, len(self.curve.curve.ctrlpts))
        self.curve.curvePts = self.curve.curve.evalpts