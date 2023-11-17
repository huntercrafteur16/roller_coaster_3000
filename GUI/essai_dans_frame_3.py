import tkinter as tk
from tkinter.tix import Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
from pylab import *
from matplotlib import pyplot,style as plt
from graphiques import AnimatedGraph
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

durée_exp=5
Courbe= [0.02*x**4-x**2+3*x for x in linspace(0, durée_exp, 50)]

root=Tk()

animgraph = AnimatedGraph((0, durée_exp), (-1, max(Courbe)+0.5), "test")

graph = FigureCanvasTkAgg(animgraph.curve, master=root)

canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)

root.mainloop()