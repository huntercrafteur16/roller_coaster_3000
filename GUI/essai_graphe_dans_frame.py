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
Courbe= [0.02*x**4-x**2+3*x for x in linspace(0, durée_exp, 50)]

def animated_graph(Courbe,durée_exp):
    graph_test = AnimatedGraph((0, durée_exp), (-1, max(Courbe)+0.5), "test")  # mise en forme
    for x in range(0, len(Courbe)):
        graph_test.drawNext(durée_exp*x/len(Courbe), Courbe[x]) # dessine point par point la courbe
        pause(0.05)
    graph_test.fixDisplay()
  

def update_graph(dx):
    graph = AnimatedGraph((0, durée_exp), (-1, max(Courbe)+0.5), "test")
    graph.drawNext(durée_exp*x/len(Courbe), Courbe[x])
 
app = tk.Tk()
app.wm_title("Graphe Matplotlib dans Tkinter")
 
style.use("ggplot")
fig = Figure(figsize=(8, 5), dpi=112)
ax1 = fig.add_subplot(211)
fig.tight_layout()
 
graph = FigureCanvasTkAgg(fig, master=app)
canvas = graph.get_tk_widget()
canvas.grid(row=0, column=0)
  
ani=FuncAnimation(fig, update_graph, interval=500)
app.mainloop()
