from tkinter import RIGHT
from numpy import true_divide
from GUI.interface import Interface
from Physique.physicManager import physicManager
from GUI.graphiques import AnimatedGraph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Physique.wagon import Wagon


interface = Interface()

manager = physicManager(interface.get_pymunk_frame().winfo_width(), interface.get_pymunk_frame().winfo_height(), interface.simu,
                        interface.get_pymunk_frame())


vitesse_graph = AnimatedGraph((0, 1000), (-1e4, 1e4), "viteeeeeeeeeeeeeeesse")
graph = FigureCanvasTkAgg(
    vitesse_graph.fig, master=interface.get_graph_frame()[0])
interface.get_graph_frame()[0].pack()
canva = graph.get_tk_widget()
canva.pack()
cont = True
i = 0
while cont:
    vitesse_graph.drawNext(
        i, abs(manager.getWagon().get_chassis_velocity()))
    interface.render_GUI()
    cont = manager.process()
    i += 1
