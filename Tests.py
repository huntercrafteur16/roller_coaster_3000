"""
fichier regroupant tout les tests
"""
import ctypes
import os
import pygame
import pymunk
import pymunk.pygame_util
from GUI.graphiques import DynamicGraph
from GUI.interface import Interface
from GUI.rail_generator import Config, Canvas
from GUI.resultInterface import ResultInterface
from Physique.wagon import Wagon
from Physique.classes_travail_wagon import Box, PinJoint, GrooveJoint, Poly, PivotJoint
from Physique.classes_travail_wagon import DampedSpring, Segment, Circle, Start_line
from Physique.physicManager import physicManager
from Physique.ClasseTrain import Train
from Physique.rails import Rail
from dataLogger import dataLogger
from tkinter import filedialog as fd
### Tests###


def test_pymunk():
    space = pymunk.Space()
    b1 = pymunk.Body(1)
    b2 = pymunk.Body(2)
    pivot = PivotJoint(space, b1, b2)
    segment = Segment(space, (0, 0), (100, 0))
    circle = Circle(space, (0, 0), 1, 1,)
    start = Start_line(space, (0, 0), (100, 0))
    box = Box(space, (0, 0), (400, 200))
    poly = Poly(space, (0, 0), [(100, 0), (101, 0), (101, 1)], 1, 1, 1)
    spring = DampedSpring(space, b1, b2, (0, 0), (0, 0), 10, 100, 1)
    groove = GrooveJoint(space, b1, b2, (100, 200), (200, 300), (100, 100))
    pinjoint = PinJoint(space, b1, b2, (0, 1))
    x0, y0 = (0, 0)
    x1, y1 = (400, 200)
    pts = [(x0, y0), (x1, y0+20), (x1, y1+20), (x0, y1)]
    assert pivot.collide is False
    assert segment.body.position == (0, 0)
    assert circle.body.position == (0, 0)
    assert start.position == (0, 0)
    assert box.points == pts
    assert poly.vertices == [(100, 0), (101, 0), (101, 1)]
    assert spring.stif == 100
    assert groove.anchor_b == (100, 100)
    assert pinjoint.a == (0, 1)


def test_physicmanager():
    space = pymunk.Space()

    manager = physicManager(1000, 600)
    assert isinstance(manager, physicManager)

    rail = Rail()
    assert isinstance(rail, Rail)
    assert not rail.data_points
    rail.addPoint((0, 0))
    assert rail.data_points == [(0, 0, 'FREE')]
    rail._addPropRail((0, 0), (100, 0), space)
    assert isinstance(rail.segments[0], pymunk.Segment)
    rail._addFreeRail((0, 0), (100, 0), space)
    assert isinstance(rail.segments[1], pymunk.Segment)
    rail._addPullRail((0, 0), (100, 0), space)
    assert isinstance(rail.segments[2], pymunk.Segment)
    rail._addBrakeRail((0, 0), (100, 0), space)
    assert isinstance(rail.segments[3], pymunk.Segment)

    space = pymunk.Space()
    wag = Wagon(space, 5, 40, 30, (300, 150))
    train = Train(space, wag, 2)
    assert isinstance(train.liste_wagon, list)
    assert isinstance(train.liste_wagon[0], Wagon)
    assert isinstance(train.liste_wagon[1], Wagon)
    assert train.liste_wagon[0] == wag
    assert train.liste_wagon[1].L == train.liste_wagon[0].L
    assert train.liste_wagon[1].h == train.liste_wagon[0].h
    assert train.liste_wagon[1].m == train.liste_wagon[0].m
    assert len(train.liste_wagon) == 2

    space = pymunk.Space()
    wag = Wagon(space, 5, 40, 30, (300, 150))
    assert isinstance(wag.w1, pymunk.shapes.Circle)
    assert isinstance(wag.w2, pymunk.shapes.Circle)
    assert isinstance(wag.w3, pymunk.shapes.Circle)
    assert isinstance(wag.w4, pymunk.shapes.Circle)
    assert isinstance(wag.c, pymunk.body.Body)
    assert isinstance(wag.L, int)
    assert wag.L == 40
    assert isinstance(wag.h, int)
    assert wag.h == 30
    assert isinstance(wag.m, int)
    assert wag.m == 5
    assert wag.c.position == (300, 150)


d = {"show_results": 1, "open": 1, "apply": 1, "play_pause": 1, "start_reset": 1}
# interface = Interface(d)
# assert isinstance(interface, Interface)


def test_config():
    config = Config()
    assert isinstance(config, Config)
    assert config.fill == (255, 255, 255)
    assert config.width == 2
    assert config.restrict is False
    assert config.restrict_zone == (160, 200, 560, 600)
    assert config.show_points is True


def test_canvas():
    screen = pygame.Surface((0, 0))
    canvas = Canvas(screen)
    assert canvas.screen == screen
    assert canvas.spline.degree == 2
    assert canvas.spline.delta == 1e-3
    assert not canvas.ctrl_points
    assert not canvas.curve_points
    assert not canvas.maindata
    assert canvas.count == 0
    assert canvas.selected is None
    assert canvas.move_point is False
    assert canvas.add_mode == 0
    assert not canvas.lineselection


def test_result_interface():
    result = ResultInterface(1, 'test')
    assert isinstance(result, ResultInterface)
    assert result.subplt_nbr == 1
    assert result.subplt_titles == 'test'


def test_interface():

    def play_pause_sim():
        "pause ou reactive physicmanger selon son état précédent "
        if manager.isPaused:
            manager.play()
        else:
            manager.pause()

    def update_sim():
        "reinitialise physicmanager avec les nouveaux paramètres"
        dyn_graphs.clear()
        logger.reset()
        param = interface.get_param()
        manager.reinit(param)

    def open_file():
        """
        Donne le fichier à ouvrir à physicManager
        """
        filename = fd.askopenfilename()
        manager.import_rails_from_file(filename)
        update_sim()

    def show_results():
        """affiche les résultats"""
        logger.render_result()

    # dictionnaire qui connecte les fonctions des boutons de l'affichade tkinter
    dict_func = {
        "start_reset": update_sim,
        "play_pause": play_pause_sim,
        "apply": update_sim,
        "open": open_file,
        "show_results": show_results,
    }
    # génération de l'objet générant l'interface principal
    interface = Interface(dict_func)

    logger = dataLogger()
    # génération du physicManager
    manager = physicManager(1920, 700,
                            interface.simu, interface.get_pymunk_frame(), logger=logger)

    # graphe de représentation de vitesse

    dyn_graphs = DynamicGraph(interface.get_graph_frame(), 2,
                              plot_titles=["énergie mécanique en J", "vitesse en m/s"])

    # continuer l'exécution du programme

    GUI_cont, phys_cont = True, True
    update_sim()

    manager.import_rails_from_file(
        os.getcwd()+"/Saves/tracé vitesse constante.txt")
    update_sim()
    manager.v = 1500
    manager.play()
    while True:
        while phys_cont and GUI_cont:

            dyn_graphs.update_data(manager.getTime(), [
                manager.get_total_train_energy()/physicManager.ppm,
                manager.get_loco_velocity()/physicManager.ppm])

            GUI_cont = interface.render_GUI()
            phys_cont = manager.process()

        if not phys_cont:
            show_results()
            update_sim()
            logger.reset()
            phys_cont = True
            manager.pause()
            break


def test_railGenerator():
    ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1920, 700))
    canvas = Canvas(screen)

    def update():
        """
        Met à jour l'affichage
        """
        screen.fill((200, 255, 255))
        canvas.render()
        pygame.display.update()
    update()
    pygame.quit()
