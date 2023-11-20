"""Fichier principal du programme"""
import time
from GUI.interface import Interface
from GUI.graphiques import AnimatedGraph
from Physique.physicManager import physicManager
global manager
global graphs


def reset_sim():
    global manager
    global graphs
    print("okok")
    manager.reinit()
    for graph in graphs:
        graph.reset()


def play_pause_sim():
    if manager.isPaused:
        manager.play()
    else:
        manager.pause()


dict_func = {
    "start_reset": reset_sim,
    "play_pause": play_pause_sim
}

interface = Interface(dict_func)
interface.start_reset_button_function = reset_sim
# génération de l'objet générant l'interface principal


# génération du physicManager
manager = physicManager(interface.get_pymunk_frame().winfo_width(),
                        interface.get_pymunk_frame().winfo_height(),
                        interface.simu, interface.get_pymunk_frame())

# graphe de représentation de vitesse
vitesse_graph = AnimatedGraph("viteeeeeeeeeeeeeeesse")
graphs = [vitesse_graph]
# on le connecte à la frame tkinter voulue
vitesse_graph.attach_to_frame(interface.get_graph_frame()[0])

# On n'oublie pas de pack le conteneur et  il faudra le faire directement dans interface
interface.get_graph_frame()[0].pack()


manager.play()
cont = True  # continuer l'exécution du programme
i = 0
while cont:

    '''
    if i > 50 and not manager.isPaused:
        manager.pause()
    if i > 70 and manager.isPaused:
        manager.play()
    '''

    vitesse_graph.drawNext(
        manager.getTime(), abs(manager.getWagon().get_chassis_velocity()))
    i += 1
    GUI_cont = interface.render_GUI()
    phys_cont = manager.process()
    cont = GUI_cont and phys_cont
