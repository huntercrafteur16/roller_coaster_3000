from time import sleep
from pylab import *
<<<<<<< HEAD
from matplotlib import *
=======
from matplotlib import pyplot as plt
>>>>>>> GUI_Martin

# On veut afficher le graphe en direct, pendant l'animation du wagon.
# Pour cela on modélise la courbe par sa liste des vitesses discrétisée par dt
# et on affiche


def graphe_vitesse(List_speeds, tf):
<<<<<<< HEAD
    # axe des temps discrétisé comme la liste des vitesses
    fig = plt.figure()
=======
    ion()  # début animation
    # axe des temps discrétisé comme la liste des vitesses
>>>>>>> GUI_Martin
    t = linspace(0, tf, len(List_speeds))
    # une reference a la courbe est mise dans line
    line, = plot(t, List_speeds)

    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1, 5)                          # mise en forme
    ylabel('vitesse')
    plt.grid()
    plt.title("Graphe des vitesses")

<<<<<<< HEAD
    return fig
# graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0,5,50)],5)


def graphe_accel(List_accels, tf):
    # axe des temps discrétisé comme la liste des accel
    fig = plt.figure()
    t = linspace(0, tf, len(List_accels))
    # une reference a la courbe est mise dans line
    line, = plot(t, List_accels)

    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1, 20)                          # mise en forme
    ylabel('accélération')
    plt.grid()
    plt.title("Graphe de l'accélération")

    return fig


def graphe_vitesse_backup(List_speeds, tf):
    ion()  # début animation
    # axe des temps discrétisé comme la liste des vitesses
    t = linspace(0, tf, len(List_speeds))
    # une reference a la courbe est mise dans line
    line, = plot(t, List_speeds)

    xlim(-0.5, tf+0.5)
    xlabel('temps')
    ylim(-1, 20)                          # mise en forme
    ylabel('vitesse')
    plt.grid()
    plt.title("Graphe des vitesses")

=======
>>>>>>> GUI_Martin
    for i in range(len(List_speeds)):
        line.set_xdata(t[:i])  # actualise les valeurs de t
        line.set_ydata(List_speeds[:i])  # actualise les valeurs de v
        draw()  # force le dessin de la figure
<<<<<<< HEAD
        pause(0.05)
    ioff()
    show()
=======
        pause(0.5)
    ioff()
    show()


class AnimatedGraph():
    def __init__(self, tlim: tuple, datalim: tuple, title) -> None:
        self.t = []
        self.data = []
        self.plt = plt
        self.plt.xlim(tlim)
        self.plt.ylim(datalim)
        self.plt.title = title
        self.plt.ion()
        self.curve, = self.plt.plot(self.t, self.data)

    def drawNext(self, t, data) -> None:

        self.t.append(t)
        self.data.append(data)
        self.curve.set_xdata(self.t)
        self.curve.set_ydata(self.data)
        self.plt.draw()

    def reset(self):
        self.t = np.array([])
        self.data = np.array([])
        self.curve.set_xdata([])
        self.curve.set_ydata([])
        self.plt.draw()

    def fixDisplay(self):
        self.plt.ioff()
        self.plt.show()


# graphe_vitesse([0.02*x**4-x**2+3*x for x in linspace(0, 5, 50)], 5)
graph_test = AnimatedGraph((0, 10), (-5, 5), "test")

for x in range(0, 100):
    graph_test.drawNext(x/10, sin(x))
    pause(0.05)
graph_test.fixDisplay()
>>>>>>> GUI_Martin
