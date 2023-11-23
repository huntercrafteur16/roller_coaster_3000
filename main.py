"""Fichier principal du programme"""

from tkinter import filedialog as fd
from GUI.interface import Interface
from GUI.graphiques import DynamicGraph
from Physique.physicManager import physicManager
from dataLogger import dataLogger


manager: physicManager
dyn_graphs: DynamicGraph
logger: dataLogger


def play_pause_sim():
    "pause ou reactive physicmanger selon son état précédent "
    if manager.isPaused:
        manager.play()
    else:
        manager.pause()


def update_sim():
    "reinitialise physicmanager avec les nouveaux paramètres"
    global dyn_graphs
    dyn_graphs.clear()
    global logger
    logger.reset()
    global interface
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
    global logger
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
manager.pause()
while True:
    while phys_cont and GUI_cont:

        dyn_graphs.update_data(manager.getTime(), [
            manager.get_total_train_energy()/physicManager.ppm,
            manager.get_loco_velocity()/physicManager.ppm])

        GUI_cont = interface.render_GUI()
        phys_cont = manager.process()

    if not GUI_cont:
        break
    if not phys_cont:
        show_results()
        update_sim()
        logger.reset()
        phys_cont = True
        manager.pause()
