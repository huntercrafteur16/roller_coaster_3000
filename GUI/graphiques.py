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
        ion()
        self.curve, = plt.plot(self.t, self.data)

    def drawNext(self, t, data) -> None: # actualise les données du graphiques à l'instant t
        xlim((0, t))

        if self._ymax <= abs(data):
            ylim((-abs(data), abs(data)))
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
