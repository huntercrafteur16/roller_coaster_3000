from time import sleep
from pylab import *
from matplotlib import pyplot as plt

# On veut afficher le graphe en direct, pendant l'animation du wagon.
# Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
# et on affiche


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
    def __init__(self, tlim: tuple, datalim: tuple, title) -> None:
        self.t = []
        self.data = []
        self.fig = plt.figure()
        xlim(tlim)
        ylim(datalim)
        ion()
        self.curve, = plt.plot(self.t, self.data)
        plt.title = title

    def drawNext(self, t, data) -> None:

        self.t.append(t)
        self.data.append(data)
        self.curve.set_xdata(self.t)
        self.curve.set_ydata(self.data)
        draw()

    def reset(self):
        self.t = np.array([])
        self.data = np.array([])
        self.curve.set_xdata([])
        self.curve.set_ydata([])
        draw()

    def fixDisplay(self):
        ioff()
        show()

# graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0, 5, 50)], 5)


durée_exp = 5
Courbe1 = [0.02*x**4-x**2+3*x for x in linspace(0, durée_exp, 50)]


def animated_graph(List_speeds, xfinal):
    graph_test = AnimatedGraph(
        (0, xfinal), (-1, max(List_speeds)+0.5), "test")  # mise en forme
    for x in range(0, len(List_speeds)):
        # dessine point par point la courbe
        graph_test.drawNext(xfinal*x/len(List_speeds), List_speeds[x])
        pause(0.05)
    graph_test.fixDisplay()  # affiche le graphe

# animated_graph(Courbe1,durée_exp)


def graphe_image_par_image(List_speeds, xfinal):
    t = linspace(0, tf, len(List_speeds))

    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1, 5)                          # mise en forme
    ylabel('vitesse')
    plt.grid()
    plt.title("Graphe des vitesses")

    for i in range(len(List_speeds)):
        plt.plot(t[:i], List_speeds[i])
        pause(0.5)
    ioff()
    show()
