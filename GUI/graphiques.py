"""Module gérant les classes animate graph et dynamic graph pour l'affichage
 des graphiques tkinter"""

from tkinter import Frame
import numpy as np
from pylab import xlim, ylim, draw, ioff, show
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# On veut afficher le graphe en temps réel, pendant l'animation du wagon.
# Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
# et on bidouille


class DynamicGraph:
    """Affichage dynamique des graphes dans tkinter"""

    def __init__(self, master, num_subplots=1, plot_titles=None):
        "intialise le dynamic graph qui prend des subplots en argument et leur nom"
        self.nbr_frames_before_show = 100
        self.curr_frames_before_show = self.nbr_frames_before_show
        self.master = master

        self.fig, self.axes = plt.subplots(1, num_subplots, sharex=True)
        # il faut s'assurer que self.axes est un tableau numpy même si num_subplots est 1
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

        # Ajuste la disposition de la figure pour plusieurs subplots
        if num_subplots > 1:
            self.fig.subplots_adjust(hspace=0.5)
        self.y_datas = [[] for _ in range(num_subplots)]
        plt.ion()

    def add_subplot(self, title="New Plot"):
        "ajoute un nouveau subplot au plot principal"
        if len(self.axes) < 3:
            ax = self.fig.add_subplot(1, len(self.axes) + 1, len(self.axes)
                                      + 1, sharex=self.axes[0], title=title)
            self.axes = np.append(self.axes, ax)

            self.plot_titles.append(title)
            self.lines.append(ax.plot([], [], )[0])
            self.fig.tight_layout()
            self.update_legend()

    def update_data(self, time: float, y_data: list[float]):
        "rajoute les données fournis"
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
        "met à jour la légende"
        for ax in self.axes:
            ax.legend(self.lines, self.plot_titles,
                      loc='upper left', bbox_to_anchor=(1, 1))

    # def show(self):
    #     plt.show()

    def clear(self):
        "reset l'affichage"
        self.x_data = []  # Clear x-data

        for i, line in enumerate(self.lines):
            line.set_ydata([])  # Clear y-data for each line
            line.set_xdata([])
            self.y_datas[i] = []  # Clear y-data in the y_datas list

        for ax in self.axes:
            ax.relim()
            ax.autoscale_view()
