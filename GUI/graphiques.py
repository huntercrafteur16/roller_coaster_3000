from cProfile import label
import numpy as np
from matplotlib.figure import Figure
import tkinter as tk
from time import sleep
from tkinter import Frame
from pylab import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# On veut afficher le graphe en temps réel, pendant l'animation du wagon.
# Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
# et on bidouille


def graphe_vitesse(List_speeds, tf):
    ion()  # début animation
    # axe des temps discrétisé comme la liste des vitesses
    t = linspace(0, tf, len(List_speeds))
    # une reference a la courbe est mise dans line
    line, = plot(t, List_speeds)

    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1, 5)                          # mise en forme
    ylabel('vitesse')
    plt.grid()
    plt.title("Graphe des vitesses")

    for i in range(len(List_speeds)):
        line.set_xdata(t[:i])  # actualise les valeurs de t
        line.set_ydata(List_speeds[:i])  # actualise les valeurs de v
        draw()  # force le dessin de la figure
        pause(0.5)
    ioff()
    show()


class AnimatedGraph():
    """
    Classe qui permet de réaliser des graphes à animer sous tkinter avec des données envoyées en temps réel
    """

    def __init__(self, title) -> None:
        self.t = []
        self.data = []
        self.fig = plt.figure()
        self._ymax = 0
        xlim(0, 0)
        plt.title(title)

        self.curve, = plt.plot(self.t, self.data)

    def drawNext(self, t, data) -> None:  # actualise les données du graphiques à l'instant t
        xlim((0, t))

        if self._ymax <= abs(data):
            ylim((-abs(data), abs(data)))
            self._ymax = abs(data)
        self.t.append(t)  # type: ignore
        self.data.append(data)  # type: ignore
        self.curve.set_xdata(self.t)
        self.curve.set_ydata(self.data)
        draw()

    def reset(self):
        self.t = []
        self.data = []
        self.curve.set_xdata([])
        self.curve.set_ydata([])
        draw()

    def fixDisplay(self):
        ioff()
        show()

    def attach_to_frame(self, frame: Frame):
        FigureCanvasTkAgg(
            self.fig, frame).get_tk_widget().pack()


class DynamicGraph:
    def __init__(self, master, num_subplots=1, plot_titles=None):
        self.nbr_frames_before_show = 100
        self.curr_frames_before_show = self.nbr_frames_before_show
        self.master = master
        self.fig, self.axes = plt.subplots(num_subplots, 1, sharex=True)
        # Ensure self.axes is a numpy array even if num_subplots is 1
        if not isinstance(self.axes, np.ndarray):
            self.axes = np.array([self.axes])

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill='both')

        self.num_subplots = num_subplots
        self.plot_titles = plot_titles or [
            f"Plot {i+1}" for i in range(num_subplots)]

        self.lines = [ax.plot([], [], label=title)[0]
                      for ax, title in zip(self.axes, self.plot_titles)]
        self.x_data = []

        # Adjust the figure layout for multiple subplots
        if num_subplots > 1:
            self.fig.subplots_adjust(hspace=0.5)
        self.y_datas = [[] for _ in range(num_subplots)]
        plt.ion()

    def add_subplot(self, title="New Plot"):
        if len(self.axes) < 3:
            ax = self.fig.add_subplot(1,
                                      len(self.axes) + 1, len(self.axes) + 1, sharex=self.axes[0], title=title)
            self.axes = np.append(self.axes, ax)

            self.plot_titles.append(title)
            self.lines.append(ax.plot([], [], )[0])
            self.fig.tight_layout()
            self.update_legend()

    def update_data(self, time, y_data):
        self.x_data.append(time)
        for line in self.lines:
            line.set_xdata(self.x_data)

        for i, ax in enumerate(self.axes):

            line = self.lines[i]
            if len(self.y_datas) > i:
                self.y_datas[i].append(y_data[i])
            else:
                self.y_datas.append([y_data[i]])
            line.set_ydata(self.y_datas[i])
            ax.relim()
            ax.autoscale_view()

    def update_legend(self):
        for ax in self.axes:
            ax.legend(self.lines, self.plot_titles,
                      loc='upper left', bbox_to_anchor=(1, 1))

    def show(self):
        plt.show()


# graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0, 5, 50)], 5)


# def animated_graph(List_speeds, xfinal):
#     graph_test = AnimatedGraph(
#         (0, xfinal), (-1, max(List_speeds)+0.5), "test")  # mise en forme
#     for x in range(0, len(List_speeds)):
#         # dessine point par point la courbe
#         graph_test.drawNext(xfinal*x/len(List_speeds), List_speeds[x])
#         pause(0.05)
#     graph_test.fixDisplay()  # affiche le graphe

# animated_graph(Courbe1,durée_exp)
