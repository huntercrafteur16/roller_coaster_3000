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


t = linspace(0, 100, 1000)
y = np.sin(0.1*t**(1.5))*2**(-0.2*t)
global i
i = 0

def updateGraph(graph: AnimatedGraph):
    global i
    t_curr = t[i]
    y_curr = y[i]
    graph.drawNext(t_curr, y_curr)
    i += 1
    v_curr = wagon.get_chassis_velocity()
    graph.drawNext(i, v_curr[0])

physicmanager = physicManager(600, 600)

root = Tk()

animgraph = AnimatedGraph((0, 100), (min(y)-0.5, max(y)+0.5), "test")
graph = FigureCanvasTkAgg(animgraph.fig, master=root)
physicmanager.update_func = partial(
    updateGraph, animgraph, wagon)  # type: ignore
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)

cont = True
while cont == True:
    cont = physicmanager.process()
    root.update()
