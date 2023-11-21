"""Fichier principal du programme"""
from tkinter import filedialog as fd
from GUI.interface import Interface
from GUI.graphiques import AnimatedGraph, DynamicGraph
from Physique.physicManager import physicManager

global manager
global graphs
global interface
manager: physicManager
graphs: list[AnimatedGraph]


def reset_sim():
    global manager
    global graphs
    manager.reinit()
    manager.play()
    for graph in graphs:
        graph.reset()


def play_pause_sim():
    if manager.isPaused:
        manager.play()
    else:
        manager.pause()


def update_sim():
    global interface
    param = interface.get_param()
    manager.reinit(param)
    manager.play()


def open_file():
    """
    Donne le fichier à ouvrir à physicManager
    """
    filename = fd.askopenfile()
    manager.import_rails_from_file(filename.name)
    manager.reinit()
    manager.play()


# dictionnaire qui connecte les fonctions des boutons de l'affichade tkinter
dict_func = {
    "start_reset": reset_sim,
    "play_pause": play_pause_sim,
    "apply": update_sim,
    "open": open_file
}
# génération de l'objet générant l'interface principal
interface = Interface(dict_func)
interface.start_reset_button_function = reset_sim


# génération du physicManager
manager = physicManager(1800, 550,
                        interface.simu, interface.get_pymunk_frame())

# graphe de représentation de vitesse

dyn_graphs = DynamicGraph(interface.get_graph_frame(), 2,
                          plot_titles=["energie", "vitesse"])


cont = True  # continuer l'exécution du programme

while cont:
    dyn_graphs.update_data(manager.getTime(), [
        manager.getWagon().get_total_energy(), manager.getWagon().get_chassis_velocity()[0]])

    GUI_cont = interface.render_GUI()
    phys_cont = manager.process()
    cont = GUI_cont and phys_cont
