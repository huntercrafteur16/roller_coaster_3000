"""Module gérant les classes animate graph et dynamic graph pour l'affichage des graphiques tkinter"""
from tkinter import Frame
import numpy as np
from pylab import xlim, ylim, draw, ioff, show
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# On veut afficher le graphe en temps réel, pendant l'animation du wagon.
# Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
# et on bidouille


class AnimatedGraph():
    """
    Classe qui permet de réaliser des graphes à animer sous tkinter avec des données envoyées en temps réel
    """

    def __init__(self, title) -> None:
        self.t = []
        self.data = []
        self.fig = plt.figure()
        self._ymax = 0
        self._ymin = 0
        xlim(0, 0)
        plt.title(title)
        plt.ion()
        self.curve, = plt.plot(self.t, self.data)

    def drawNext(self, t, data) -> None:
        """actualise les données du graphiques à l'instant t"""
        xlim((0, t))

        if self._ymax < data:
            self._ymax = data
            ylim((self._ymin, data))
        if self._ymin > data:
            self._ymin = data
            ylim((data, self._ymax))
        self.t.append(t)  # type: ignore
        self.data.append(data)  # type: ignore
        self.curve.set_xdata(self.t)
        self.curve.set_ydata(self.data)
        draw()

    def reset(self):
        """reset l'affichage du graphique"""
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
    """Affichage dynamique des graphes dans tkinter"""

    def __init__(self, master, num_subplots=1, plot_titles=None):
        "intialise le dynamic graph qui prend des subplots en argument et leur nom"
        self.nbr_frames_before_show = 100
        self.curr_frames_before_show = self.nbr_frames_before_show
        self.master = master

        self.fig, self.axes = plt.subplots(1, num_subplots, sharex=True)
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
        "ajoute un nouveau subplot au plot principal"
        if len(self.axes) < 3:
            ax = self.fig.add_subplot(1,
                                      len(self.axes) + 1, len(self.axes) + 1, sharex=self.axes[0], title=title)
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
        try:
            self.x_data = []  # Clear x-data

            for i, line in enumerate(self.lines):
                line.set_ydata([])  # Clear y-data for each line
                self.y_datas[i] = []  # Clear y-data in the y_datas list

            for ax in self.axes:
                ax.relim()
                ax.autoscale_view()
        except:
            pass
