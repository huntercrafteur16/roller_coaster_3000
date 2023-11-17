from tkinter import RIGHT
from numpy import true_divide
from GUI.interface import Interface
from Physique.physicManager import physicManager
from GUI.graphiques import AnimatedGraph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Physique.wagon import Wagon

interface = Interface()  # génération de l'objet génrant l'interface principal

manager = physicManager(interface.get_pymunk_frame().winfo_width(), interface.get_pymunk_frame().winfo_height(), interface.simu,
                        interface.get_pymunk_frame())  # génération du physicManager

# graphe de représentation de vitesse
vitesse_graph = AnimatedGraph("viteeeeeeeeeeeeeeesse")

# on le connecte à la frame tkinter voulue
vitesse_graph.attach_to_frame(interface.get_graph_frame()[0])

# On n'oublie pas de pack le conteneur et #TODO il faudra le faire directement dans interface
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
