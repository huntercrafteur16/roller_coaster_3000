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


def update_graph(dt):
    x, y1, y2 = get_back_values()
    ax1.clear()
    ax2.clear()
    ax1.set_ylim(0, 10, auto=False)
    ax2.set_ylim(0, 10, auto=False)
    ax2.set_xlabel('Temps')
    ax1.set_ylabel('tension', color='g')
    ax2.set_ylabel('courant', color='r')
    ax1.plot(x, y1, 'g-o')
    ax2.plot(x, y2, 'r-o')

app = tk.Tk()
app.wm_title("Graphe Matplotlib dans Tkinter")
 
style.use("ggplot")
fig = Figure(figsize=(8, 5), dpi=112)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_xlabel('Temps')
ax1.set_ylabel('tension', color='g')
ax2.set_ylabel('courant', color='r')
fig.tight_layout()