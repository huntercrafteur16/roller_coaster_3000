"""Fichier principal du programme"""
from GUI.interface import Interface
from GUI.graphiques import AnimatedGraph
from Physique.physicManager import physicManager
from tkinter import filedialog as fd

global manager
global graphs
global interface
manager: physicManager
graphs: list[AnimatedGraph]


def reset_sim():
    global manager
    global graphs
    manager.reinit()
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


def open_file():

    filename = fd.askopenfile()

    manager.import_rails_from_file(filename.name, 50)


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
manager = physicManager(interface.get_pymunk_frame().winfo_width(),
                        interface.get_pymunk_frame().winfo_height(),
                        interface.simu, interface.get_pymunk_frame())

# graphe de représentation de vitesse
vitesse_graph = AnimatedGraph("vitesse")
acceleration_graph = AnimatedGraph("accelération")
energie_graph = AnimatedGraph("énergie")

graphs = [vitesse_graph, acceleration_graph, energie_graph]
# on le connecte à la frame tkinter voulue
vitesse_graph.attach_to_frame(interface.get_graph_frame("vitesse"))
acceleration_graph.attach_to_frame(
    interface.get_graph_frame("acceleration"))
energie_graph.attach_to_frame(
    interface.get_graph_frame("energie"))

manager.play()
cont = True  # continuer l'exécution du programme

while cont:

    vitesse_graph.drawNext(
        manager.getTime(), abs(manager.getWagon().get_chassis_velocity()))
    acceleration_graph.drawNext(
        manager.getTime(), abs(manager.getWagon().get_chassis_acceleration()))
    energie_graph.drawNext(
        manager.getTime(), abs(manager.getWagon().get_total_energy()))
    
    interface.affiche_frame_voulue() # fonction qui affiche ou non la frame en fonction de la valeur du radio button

    GUI_cont = interface.render_GUI()
    phys_cont = manager.process()
    cont = GUI_cont and phys_cont
