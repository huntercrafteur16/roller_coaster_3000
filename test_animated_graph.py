from functools import partial
import tkinter as tk
from tkinter.tix import Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylab import *
from matplotlib import pyplot, style as plt
from GUI.graphiques import AnimatedGraph
import tkinter as tk
import Physique.wagon
import Physique.classes_travail_wagon
from Physique.physicManager import physicManager

global i
i = 0


def updateGraph(graph: AnimatedGraph, wagon: Physique.wagon.Wagon):
    global i
    i += 1
    v_curr = wagon.get_chassis_velocity()
    graph.drawNext(i, abs(v_curr))


physicmanager = physicManager(600, 600)
wagon = physicmanager.getWagon()


root = Tk()

animgraph = AnimatedGraph((0, 1000), (-1e3, 1e3), "test")
graph = FigureCanvasTkAgg(animgraph.fig, master=root)
physicmanager.updateFunc = partial(
    updateGraph, animgraph, wagon)  # type: ignore
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)

cont = True
while cont == True:
    cont = physicmanager.process()
    root.update()
