import sys
from geomdl import BSpline
from geomdl import utilities
from math import *

import pygame
from Physique.rails import Rail
from geomdl import BSpline

import tkinter as tk
from tkinter import filedialog


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
        self.presel = False
        self.lineselection = []
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
        self.save_open_button = (6*width/8, height - 50, 50, 20)
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

            if len(self.lineselection) == 2:
                pygame.draw.rect(
                    self.screen, self.cfg.bright, self.free_type_button)
                text_surface = self.my_font.render(
                    'libre', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.free_type_button[0], self.free_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright, self.brake_type_button)
                text_surface = self.my_font.render(
                    'frein', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.brake_type_button[0], self.brake_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright, self.pull_type_button)
                text_surface = self.my_font.render(
                    'treuil', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.pull_type_button[0], self.pull_type_button[1]+20))

                pygame.draw.rect(
                    self.screen, self.cfg.bright, self.prop_type_button)
                text_surface = self.my_font.render(
                    'entraîner', False, (0, 0, 0))
                self.screen.blit(
                    text_surface, (self.prop_type_button[0], self.prop_type_button[1]+20))

            pygame.draw.rect(self.screen, self.cfg.dark, self.hide_button)
            text_surface = self.my_font.render(
                'montrer/cacher', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.hide_button[0], self.hide_button[1]+20))

            pygame.draw.rect(self.screen, self.cfg.dark, self.save_open_button)
            text_surface = self.my_font.render(
                'enregistrer', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (self.save_open_button[0], self.save_open_button[1]+20))

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
            if self.count >= self.spline.degree+1:
                for i in range(len(self.maindata)-1):
                    pt1 = self.maindata[i]
                    pt2 = self.maindata[i+1]
                    if len(self.lineselection) == 2 and i > self.lineselection[0] and i < self.lineselection[1]:
                        pygame.draw.lines(self.screen, (0, 255, 255), 0, [
                                          pt1[0], pt2[0]], width=self.cfg.width)

                    elif pt2[1] == "FREE":
                        pygame.draw.lines(self.screen, (50, 50, 50), 0, [
                                          pt1[0], pt2[0]], width=self.cfg.width)
                    elif pt2[1] == "PROP":
                        pygame.draw.lines(self.screen, (0, 255, 0), 0, [
                                          pt1[0], pt2[0]], width=self.cfg.width)
                    elif pt2[1] == "PULL":
                        pygame.draw.lines(self.screen, (255, 150, 0), 0, [
                                          pt1[0], pt2[0]], width=self.cfg.width)
                    elif pt2[1] == "BRAKE":
                        pygame.draw.lines(self.screen, (255, 0, 0), 0, [
                                          pt1[0], pt2[0]], width=self.cfg.width)

                # la courbe calculée, sans zone sélectionnée
                # if len(self.lineselection) < 2:
                #    pygame.draw.lines(self.screen, self.cfg.color,
                #                      0, self.curve_points, width=self.cfg.width)

                # la courbe calculée, avec une zone de sélection bleue
                # else:
                #    if self.lineselection[0] != 0:
                #        pygame.draw.lines(
                #            self.screen, self.cfg.color, 0, self.curve_points[:self.lineselection[0]+1], width=self.cfg.width)
                #    pygame.draw.lines(
                #        self.screen, self.cfg.sea, 0, self.curve_points[self.lineselection[0]:self.lineselection[1]+1], width=self.cfg.width)
                #    if self.lineselection[1] != len(self.curve_points)-1:
                #        pygame.draw.lines(
                #            self.screen, self.cfg.color, 0, self.curve_points[self.lineselection[1]:], width=self.cfg.width)
        self.button_render()

    def region(self, button, x, y):
        bx, by, brx, bry = button
        if bx < x < bx+brx and by < y < by+bry:
            return True
        return False

    def select_left(self, x, y, r=10):
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
                    self.selected -= 1
                    can_add = False
                    if self.count >= 3:
                        self.draw(self.ctrl_points)
            elif self.region(self.save_open_button, x, y):
                print("souvegarde")
                self.save_file()

            elif len(self.lineselection) == 2:
                if self.region(self.free_type_button, x, y):
                    self.selected = None
                    can_add = False
                    for point in self.maindata[self.lineselection[0]:(self.lineselection[1]+1)]:
                        point[1] = "FREE"
                    print("FREE")

                elif self.region(self.brake_type_button, x, y):
                    self.selected = None
                    can_add = False
                    for point in self.maindata[self.lineselection[0]:(self.lineselection[1]+1)]:
                        point[1] = "BRAKE"
                    print("BRAKE")

                elif self.region(self.prop_type_button, x, y):
                    self.selected = None
                    can_add = False
                    for point in self.maindata[self.lineselection[0]:(self.lineselection[1]+1)]:
                        point[1] = "PROP"
                    print("PROP")

                elif self.region(self.pull_type_button, x, y):
                    self.selected = None
                    can_add = False
                    for point in self.maindata[self.lineselection[0]:(self.lineselection[1]+1)]:
                        point[1] = "PULL"
                    print("PULL")

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
                if self.count >= 3:
                    self.draw(self.ctrl_points)

        elif self.region(self.edit_button, x, y):
            self.cfg.edit_mode = True

            # file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[
            #                                          ("Text files", "*.txt"), ("All files", "*.*")])
            # if file_path:
            #     with open(file_path, 'w') as file:
            #         content = "\n".join(
            #             [f"{point[0]},{point[1]}" for point in self.ctrl_points])
            #         file.write(content)

            # elif self.region(self.save_open_button, x, y):
            #     self.save_file()

    def closest_point(self, x, y):
        closest_i = 0
        for i in range(len(self.curve_points)):
            if (x-self.curve_points[i][0])**2 + (y-self.curve_points[i][1])**2 < (x-self.curve_points[closest_i][0])**2 + (y-self.curve_points[closest_i][1])**2:
                closest_i = i
        return closest_i

    def select_right(self, x, y):
        if self.presel == True and self.closest_point(x, y) != self.lineselection[0]:
            if self.closest_point(x, y) > self.lineselection[0]:
                self.lineselection.append(self.closest_point(x, y))
            else:
                self.lineselection = [self.closest_point(
                    x, y), self.lineselection[0]]
        else:
            self.lineselection = [self.closest_point(x, y)]
        self.presel = not self.presel

    def move(self, xy):
        if self.move_point:
            self.ctrl_points.pop(self.selected)
            self.ctrl_points.insert(self.selected, xy)
            if self.count >= 3:
                self.draw(self.ctrl_points)

            return True

    def draw(self, curvePts):
        p0x, p0y = curvePts[0]
        L = [(p0x-40, p0y), (p0x-39, p0y)]
        self.spline.degree = self.spline.degree  # Set the degree first
        self.spline.ctrlpts = L+curvePts
        self.spline.knotvector = utilities.generate_knot_vector(
            self.spline.degree, len(self.spline.ctrlpts))
        self.curve_points = self.spline.evalpts
        if self.maindata != []:
            for i in range(len(self.maindata)):
                self.maindata[i][0] = (self.curve_points[i])
        for i in range(len(self.maindata)+1, len(self.curve_points)):
            self.maindata.append([(self.curve_points[i]), "FREE"])

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
            ("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            with open(file_path, 'w') as file:
                lines = []
                for i in range(len(self.maindata)):

                    line = str(
                        self.maindata[i][0][0])+","+str(self.maindata[i][0][1])+","+str(self.maindata[i][1])+"\n"
                    lines.append(line)
                file.writelines(lines)
            sys.exit()
