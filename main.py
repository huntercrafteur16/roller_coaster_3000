"""Fichier principal du programme"""
from GUI.interface import Interface
from GUI.graphiques import AnimatedGraph
from Physique.physicManager import physicManager


interface = Interface()  # génération de l'objet génrant l'interface principal

# génération du physicManager
manager = physicManager(interface.get_pymunk_frame().winfo_width(),
                        interface.get_pymunk_frame().winfo_height(),
                        interface.simu, interface.get_pymunk_frame())

# graphe de représentation de vitesse
vitesse_graph = AnimatedGraph("viteeeeeeeeeeeeeeesse")

# on le connecte à la frame tkinter voulue
vitesse_graph.attach_to_frame(interface.get_graph_frame()[0])

# On n'oublie pas de pack le conteneur et  il faudra le faire directement dans interface
interface.get_graph_frame()[0].pack()


cont = True  # continuer l'exécution du programme
i = 0
while cont:
    vitesse_graph.drawNext(
        i, abs(manager.getWagon().get_chassis_velocity()))
    GUI_cont = interface.render_GUI()
    phys_cont = manager.process()
    cont = GUI_cont and phys_cont
    i += 1
