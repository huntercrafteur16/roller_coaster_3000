"""
Module qui permet la construction personalisée des rails
"""
from tkinter import filedialog
from geomdl import BSpline
from geomdl import utilities
import pygame


class Config():
    """
    Classe qui configure la fenetre
    """

    def __init__(self):
        self.fill = (255, 255, 255)
        self.width = 2
        self.restrict = False
        self.restrict_zone = (160, 200, 560, 600)
        self.show_points = True


class Canvas():
    """
    Classe d'affichage et de création d'un objet rail pour physic manager
    """

    def __init__(self, screen: pygame.Surface):
        self.cfg = Config()
        self.screen = screen
        self.spline = BSpline.Curve()
        self.spline.degree = 2
        self.spline.delta = 1e-3

        # self.physics = Rail()
        self.ctrl_points = []
        self.curve_points = []
        # Liste de tuples de 3 variables : (x, y, "type de tracé")
        self.maindata = []
        self.count = 0
        self.selected = None
        self.move_point = False
        self.add_mode = 0
        self.lineselection = []

        # grille

        # affichage graphique
        self.my_font = pygame.font.SysFont('Comic Sans MS', 12)
        self.w, self.h = screen.get_width(), screen.get_height()
        dl = 60
        dh = 20

        self.instructions = ((7*self.w/12, self.h-60, dl, dh))
        self.save_button = (self.w/12-30, 20, dl, dh)
        self.open_button = (2*self.w/12-30, 20, dl, dh)

        self.hide_button = (self.w/12-30, self.h - 50, dl, dh)
        self.add_button = (2*self.w/12-30, self.h - 50, dl, dh)
        self.del_button = (3*self.w/12-30, self.h - 50, dl, dh)
        self.desel_button = (4*self.w/12-30, self.h - 50, dl, dh)

        self.free_type_button = ((3*self.w/12-30, self.h - 50, dl, dh))
        self.prop_type_button = ((4*self.w/12-30, self.h - 50, dl, dh))
        self.pull_type_button = ((5*self.w/12-30, self.h - 50, dl, dh))
        self.brake_type_button = ((6*self.w/12-30, self.h - 50, dl, dh))

    def button_render(self):
        """
        renvoie les informations des bouttons
        """

        text_surface = self.my_font.render(
            'Clic gauche pour sélectionner/ajouter un point. Si sélection, ajout après le point sélectionné.', False, (0, 0, 0))
        self.screen.blit(
            text_surface, (self.instructions[0], self.instructions[1]))
        text_surface = self.my_font.render(
            'Deux clics droits pour la sélection de tracé, un troisième pour désélectionner.', False, (0, 0, 0))
        self.screen.blit(
            text_surface, (self.instructions[0], self.instructions[1]+15))
        text_surface = self.my_font.render(
            'Les loopings ne marchent pas !', False, (0, 0, 0))
        self.screen.blit(
            text_surface, (self.instructions[0], self.instructions[1]+30))

        if self.add_mode:
            pygame.draw.rect(self.screen, (0, 230, 0), self.add_button)
            text_surface = self.my_font.render(
                'ajout de points', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.add_button[0], self.add_button[1]+20))
        else:
            pygame.draw.rect(
                self.screen, (150, 150, 150), self.add_button)
            text_surface = self.my_font.render(
                'ajout de points', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.add_button[0], self.add_button[1]+20))

        if self.selected is not None:
            pygame.draw.rect(self.screen, (255, 150, 0), self.desel_button)
            text_surface = self.my_font.render(
                'déselectionner', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.desel_button[0], self.desel_button[1]+20))

            pygame.draw.rect(
                self.screen, (255, 0, 0), self.del_button)
            text_surface = self.my_font.render(
                'supprimer', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.del_button[0], self.del_button[1]+20))

        elif len(self.lineselection) == 2:
            pygame.draw.rect(
                self.screen, (60, 60, 60), self.free_type_button)
            text_surface = self.my_font.render(
                'rail libre', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.free_type_button[0], self.free_type_button[1]+20))

            pygame.draw.rect(
                self.screen, (250, 0, 0), self.brake_type_button)
            text_surface = self.my_font.render(
                'frein', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.brake_type_button[0], self.brake_type_button[1]+20))

            pygame.draw.rect(
                self.screen, (250, 150, 0), self.pull_type_button)
            text_surface = self.my_font.render(
                'treuil', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.pull_type_button[0], self.pull_type_button[1]+20))

            pygame.draw.rect(
                self.screen, (220, 220, 0), self.prop_type_button)
            text_surface = self.my_font.render(
                'propulseur', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.prop_type_button[0], self.prop_type_button[1]+20))

        if self.cfg.show_points is True:
            pygame.draw.rect(self.screen, (100, 0, 200), self.hide_button)
            text_surface = self.my_font.render(
                'ossature : visible', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.hide_button[0], self.hide_button[1]+20))

        else:
            pygame.draw.rect(
                self.screen, (150, 150, 150), self.hide_button)
            text_surface = self.my_font.render(
                'ossature : cachée', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.hide_button[0], self.hide_button[1]+20))

        pygame.draw.rect(self.screen, (0, 0, 0), self.save_button)
        text_surface = self.my_font.render(
            'enregistrer sous', False, (0, 0, 0))
        self.screen.blit(
            text_surface, (self.save_button[0], self.save_button[1]+20))

        pygame.draw.rect(self.screen, (0, 0, 0), self.open_button)
        text_surface = self.my_font.render(
            'ouvrir un tracé', False, (0, 0, 0))
        self.screen.blit(
            text_surface, (self.open_button[0], self.open_button[1]+20))

    def render(self):
        """
        Renvoi les résultats
        """
        # affichage de la grille
        for n in range(0, self.w, 10):
            pygame.draw.line(self.screen, (255, 255, 255), (n, 0), (n, self.h))
        for m in range(0, self.h, 10):
            pygame.draw.line(self.screen, (255, 255, 255), (0, m), (self.w, m))

        if self.cfg.show_points:
            if self.count == 1:
                pygame.draw.circle(
                    self.screen, (0, 100, 220), self.ctrl_points[0], 5)
            elif self.count >= 2:
                pygame.draw.lines(
                    self.screen, (50, 0, 100), False, self.ctrl_points)
                # cette ligne trace les segments entre les points
                for i, point in enumerate(self.ctrl_points):
                    if i == 0:
                        pygame.draw.circle(
                            self.screen, (0, 100, 220), point, 5)
                        # le premier point du tracé
                    elif i == self.selected:
                        pygame.draw.circle(
                            self.screen, (0, 230, 0), point, 5)
                        # le point séléctionné (pour le bouger)
                    else:
                        pygame.draw.circle(
                            self.screen, (100, 0, 200), point, 5)
                        # les autres points

        if len(self.lineselection) == 2:
            self.selected = None

        if self.count >= 3:
            for i in range(len(self.maindata)-1):
                pt1 = self.maindata[i]
                pt2 = self.maindata[i+1]
                temp = self.lineselection
                if len(self.lineselection) == 2 and i > temp[0] and i < temp[1]:
                    pygame.draw.lines(self.screen, (0, 220, 220), False, [
                        pt1[0], pt2[0]], width=self.cfg.width)

                elif pt2[1] == "FREE":
                    pygame.draw.lines(self.screen, (60, 60, 60), False, [
                        pt1[0], pt2[0]], width=self.cfg.width)
                elif pt2[1] == "PULL":
                    pygame.draw.lines(self.screen, (250, 150, 0), False, [
                        pt1[0], pt2[0]], width=self.cfg.width)
                elif pt2[1] == "BRAKE":
                    pygame.draw.lines(self.screen, (250, 0, 0), False, [
                        pt1[0], pt2[0]], width=self.cfg.width)
                elif pt2[1] == "PROP":
                    pygame.draw.lines(self.screen, (220, 220, 0), False, [
                        pt1[0], pt2[0]], width=self.cfg.width)

        self.button_render()

    def region(self, button: tuple[float, float, float, float], x: float, y: float):
        """
        Renvoie si le point est sur le bouton
        """
        bx, by, brx, bry = button
        if bx < x < bx+brx and by < y < by+bry:
            return True
        return False

    def select_left(self, x: float, y: float, r=10):
        """
        Renvoie si gauche est selectionné
        """
        can_add = True
        if self.region(self.add_button, x, y):
            self.add_mode = not self.add_mode
            can_add = False
        elif self.region(self.hide_button, x, y):
            self.cfg.show_points = not self.cfg.show_points
            self.selected = None
            can_add = False

        if self.selected is not None:
            if self.region(self.desel_button, x, y):
                can_add = False
                self.selected = None
            elif self.region(self.del_button, x, y):
                can_add = False
                if self.selected:
                    self.ctrl_points.pop(self.selected)
                    self.count -= 1
                    self.selected -= 1
                    if self.count >= 3:
                        self.draw(self.ctrl_points)

        if self.region(self.save_button, x, y):
            can_add = False
            self.save_file()

        elif self.region(self.open_button, x, y):
            can_add = False
            self.open_file()

        elif len(self.lineselection) == 2:
            self.selected = None
            can_add = None

            if self.region(self.free_type_button, x, y):
                for point in self.maindata[self.lineselection[0]+2:(self.lineselection[1]+1)]:
                    point[1] = "FREE"

            if self.region(self.brake_type_button, x, y):
                for point in self.maindata[self.lineselection[0]+2:(self.lineselection[1]+1)]:
                    point[1] = "BRAKE"

            if self.region(self.prop_type_button, x, y):
                for point in self.maindata[self.lineselection[0]+2:(self.lineselection[1]+1)]:
                    point[1] = "PROP"

            if self.region(self.pull_type_button, x, y):
                for point in self.maindata[self.lineselection[0]+2:(self.lineselection[1]+1)]:
                    point[1] = "PULL"

        if self.count:
            for i, points in enumerate(self.ctrl_points):
                px, py = points
                if px-r < x < px+r and py-r < y < py+r:

                    self.selected = i
                    self.move_point = True
                    can_add = False

        if self.add_mode and can_add:
            self.count += 1
            if self.selected is not None:
                xpoint, _ = self.ctrl_points[self.selected]
                self.ctrl_points.insert(self.selected+1, (x, y))
            else:
                self.ctrl_points.append((x, y))
            if self.count >= 3:
                self.draw(self.ctrl_points)

    def closest_point(self, x: float, y: float):
        """
        Renvoie le point le plus proche
        """
        cl_i = 0
        temp = self.curve_points
        for i in range(len(temp)):
            if (x-temp[i][0])**2 + (y-temp[i][1])**2 < (x-temp[cl_i][0])**2 + (y-temp[cl_i][1])**2:
                cl_i = i
        return cl_i

    def select_right(self, x: float, y: float):
        """
        Renvoie si droite est selectionné
        """
        if len(self.lineselection) == 0:
            self.lineselection = [self.closest_point(x, y)]

        elif len(self.lineselection) == 1 and self.closest_point(x, y) != self.lineselection[0]:
            if self.closest_point(x, y) > self.lineselection[0]:
                self.lineselection.append(self.closest_point(x, y))
            else:
                self.lineselection = [self.closest_point(
                    x, y), self.lineselection[0]]
        elif len(self.lineselection) == 2:
            self.lineselection = []

    def move(self, xy):
        """
        Déplace les points de controle
        """
        if self.move_point and self.selected is not None:
            self.ctrl_points.pop(self.selected)
            self.ctrl_points.insert(self.selected, xy)
            if self.count >= 3:
                self.draw(self.ctrl_points)

            return True

    def draw(self, curvePts: list):
        """
        dessine la courbe
        """
        p0x, p0y = curvePts[0]
        L = [(p0x-40, p0y), (p0x-39, p0y)]
        self.spline.degree = self.spline.degree  # Set the degree first
        self.spline.ctrlpts = L + curvePts
        self.spline.knotvector = utilities.generate_knot_vector(
            self.spline.degree, len(self.spline.ctrlpts))
        self.curve_points = self.spline.evalpts
        if self.maindata != []:
            for i in range(len(self.maindata)):
                self.maindata[i][0] = self.curve_points[i]
        for i in range(len(self.maindata)+1, len(self.curve_points)):
            self.maindata.append([(self.curve_points[i]), "FREE"])

    def save_file(self):
        """
        enregistre le fichier
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                lines = []

                # Points du tracé
                for i in range(len(self.maindata)):
                    line = str(self.maindata[i][0][0])+","+str(
                        self.maindata[i][0][1])+","+str(self.maindata[i][1])+"\n"
                    lines.append(line)

                # Points de contrôle (sert à rouvrir le fichier)
                for i in range(len(self.ctrl_points)):
                    line = str(self.ctrl_points[i][0]) + \
                        ","+str(self.ctrl_points[i][1])+"\n"
                    lines.append(line)

                file.writelines(lines)

    def open_file(self):
        """
        ouvre le fichier
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            self.maindata = []
            self.ctrl_points = []

            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip('\n')
                    line = line.split(",")

                    # Lecture des points du tracé
                    if len(line) == 3:
                        self.maindata.append(
                            [(float(line[0]), float(line[1])), line[2]])

                    # Lecture des points de contrôle
                    elif len(line) == 2:
                        self.ctrl_points.append(
                            (float(line[0]), float(line[1])))

                self.count = len(self.ctrl_points)
                self.selected = None
