from ast import List
import tkinter as tk
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
List_speeds= [0.02*x**4-x**2+3*x for x in linspace(0, durée_exp, 50)]
t = linspace(0, durée_exp, len(List_speeds))
nul=[0 for k in List_speeds]

def update_graph(dt):
    x, y1 = t,List_speeds
    ax1.clear()
    ax1.set_ylim(-1, max(List_speeds)+0.5, auto=False)
    ax1.set_xlim(0, durée_exp, auto=False)
    ax1.set_xlabel('Temps')
    ax1.set_ylabel('vitesse', color='r')
    ax1.plot(x, y1)

app = tk.Tk()
app.wm_title("Graphe Matplotlib dans Tkinter")

style.use("ggplot")
fig = Figure(figsize=(8, 5), dpi=112)
ax1 = fig.add_subplot(211)
ax1.set_ylim(-1, max(List_speeds)+0.5, auto=False)
ax1.set_xlim(0, durée_exp, auto=False)
ax1.set_xlabel('Temps')
ax1.set_ylabel('vitesse', color='r')
fig.tight_layout()

graph = FigureCanvasTkAgg(fig, master=app)
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)

anim=FuncAnimation(fig, update_graph, interval=500)
app.mainloop()