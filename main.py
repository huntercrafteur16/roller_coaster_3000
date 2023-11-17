from numpy import true_divide
from GUI.interface import Interface
from Physique.physicManager import physicManager
from GUI.graphiques import AnimatedGraph


interface = Interface()

manager = physicManager(interface.get_pymunk_frame().winfo_width(), interface.get_pymunk_frame().winfo_height(), interface.simu,
                        interface.get_pymunk_frame())


cont = True
while cont:

    interface.render_GUI()
    cont = manager.process()
