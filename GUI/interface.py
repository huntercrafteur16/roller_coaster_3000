
from tkinter import *
# from GUI.graphiques import AnimatedGraph
import time
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# On définit une classe "Interface" qui prend en argument deux dictionnaires,
# les variables et les fonctions donc l'interface a besoin pour s'implémenter


class Interface():
    play_pause_button_function: Callable
    start_reset_button_function: Callable

    isRunning: bool

    def __init__(self):
        # dimensions de la fenetre pymunk en px
        roller_coaster_width = 1600
        roller_coaster_height = 550
        # Fenêtre principale
        self.root = Tk()
        self.root.title("Bienvenue dans le Roller Coaster 3000, visiteur !")
        self.isRunning = True
        self.root.protocol('WM_DELETE_WINDOW', self.killInterface)
        # Trois frames : barre d'outils, simulation, barre des graphes
        toolbar = Frame(self.root, bg="lightgray")
        simu = Frame(self.root, borderwidth=5, bg="white")
        self.simu = simu
        graphbar = Frame(self.root, bg="lightgray")
        toolbar.pack(side=TOP, expand=False, fill=X)
        simu.pack(expand=True, fill=BOTH)
        graphbar.pack(side=BOTTOM, fill=X, expand=False)

        # Variables
        self.applied_m, self.applied_f, self.applied_c = 1, 10, 0.1
        m, f, c = DoubleVar(value=1), DoubleVar(value=10), DoubleVar(value=0.1)

        def apply_values():
            self.applied_m = float(m.get())
            self.applied_f = float(f.get())
            self.applied_c = float(c.get())

        # Boutons Start/Reset
        buttons = Frame(toolbar, bg="lightgray", height=100, padx=5)
        buttons.grid(row=0, column=0)

        def doNothing():
            pass

        self.start_reset = Button(buttons, command=self.start_reset_button_function, width=10, height=2,
                                  text='Start/Reset', fg='#30b000', activebackground='#30b000')
        self.play_pause = Button(buttons, command=self.play_pause_button_function, width=10, height=2,
                                 text='Play/Pause', fg='#0080ff', activebackground='#0080ff')
        self.start_reset.grid(row=0, column=0, padx=3, pady=3)
        self.play_pause.grid(row=0, column=1, padx=3, pady=3)

        # Paramètres
        param = Frame(toolbar, bg="lightgray", width=200, padx=5, pady=5)
        param.grid(row=0, column=1)

        apply_param = Button(param, height=2, text='Appliquer les paramètres',
                             bg='lightgray', fg='red', activebackground='red', command=apply_values)
        apply_param.grid(row=0, column=0, padx=5, pady=5)

        # masse
        param_m = Frame(param)
        label_m = Label(param_m, text='Masse des wagons (kg)',
                        width=25, height=1)
        entry_m = Entry(param_m, textvariable=m, width=5)
        scale_m = Scale(param_m, from_=0, to=100, showvalue=False, variable=m,
                        tickinterval=25, orient=HORIZONTAL, width=10)
        # vitesse
        param_F = Frame(param)
        label_F = Label(param_F, text='Force des propulseurs (N)',
                        width=25, height=1)
        entry_F = Entry(param_F, textvariable=f, width=5)
        scale_F = Scale(param_F, from_=0, to=100, showvalue=False, variable=f,
                        tickinterval=25, orient=HORIZONTAL, width=10)
        # coef de frottement
        param_f = Frame(param)
        label_f = Label(param_f, text='Coef. de frottement (kg/m)',
                        width=25, height=1)
        entry_f = Entry(param_f, textvariable=c, width=5)
        scale_f = Scale(param_f, from_=0, to=10, showvalue=False, variable=c,
                        tickinterval=2, orient=HORIZONTAL, width=10)

        # On affiche tout
        label_m.grid(row=0, column=1, columnspan=2)
        entry_m.grid(row=1, column=1, padx=3)
        scale_m.grid(row=1, column=2)
        param_m.grid(row=0, column=1, padx=10, pady=5)

        label_F.grid(row=0, column=1, columnspan=2)
        entry_F.grid(row=1, column=1, padx=3)
        scale_F.grid(row=1, column=2)
        param_F.grid(row=0, column=2, padx=10, pady=5)

        label_f.grid(row=0, column=1, columnspan=2)
        entry_f.grid(row=1, column=1, padx=3)
        scale_f.grid(row=1, column=2)
        param_f.grid(row=0, column=3, padx=10, pady=5)

        # A l'intérieur de simu : roller coaster et graphe
        self.roller_coaster = Frame(
            simu, bg='white', height=roller_coaster_height, width=roller_coaster_width)
        self.frame_graph = Frame(graphbar, bg='blue', width=100, height=50)
        self.roller_coaster.grid(
            row=1, column=1, rowspan=3, columnspan=3, sticky=N)

        # A l'intérieur de graphbar, choix des graphes.

        # Boutons radio pour voir ou non un des graphes proposés
        graph_choice = Frame(graphbar, height=80)
        graph_choice.pack(side=LEFT, expand=False, padx=5, pady=5)

        self.choice = IntVar(value=0)
        label_graph_choice = Label(
            graph_choice, text="Choix du graphe à afficher", height=2)
        label_graph_choice.grid(row=0, column=0, padx=5, pady=5)

        Radiobuttons = Frame(graph_choice, borderwidth=5)
        Radiobuttons.grid(row=1, column=0)

        Radiobutton(Radiobuttons, variable=self.choice, value='none',
                    height=1).grid(row=1, column=1, sticky=E)
        Label(Radiobuttons, text='Aucun graphe', width=15,
              height=1).grid(row=1, column=0, sticky=E)

        Radiobutton(Radiobuttons, variable=self.choice, value='speeds',
                    height=1).grid(row=2, column=1, sticky=E)
        Label(Radiobuttons, text='Vitesse(t)',
              width=15, height=1).grid(row=2, column=0, sticky=E)

        Radiobutton(Radiobuttons, variable=self.choice, value='accels',
                    height=1).grid(row=3, column=1, sticky=E)
        Label(Radiobuttons, text='Accélération(t)',
              width=15, height=1).grid(row=3, column=0, sticky=E)

        self.t_graph = DoubleVar(value=10)
        Label(Radiobuttons, text='Durée de mesure (s): ', width=15,
              height=1).grid(row=4, column=0, sticky=E)
        Entry(Radiobuttons, textvariable=self.t_graph, width=4).grid(
            row=4, column=1, sticky=E)

    # Donne la frame qui doit contenir un graphe et le choix de graphe associé
    def get_graph_frame(self):
        return (self.frame_graph, self.choice.get())

    # Donne la frame dans laquelle
    def get_pymunk_frame(self):
        return self.roller_coaster

    # Rend les valeurs choisies
    def get_param(self):
        return {'mass': self.applied_m, 'force': self.applied_f, 'frict': self.applied_c}

    def render_GUI(self) -> bool:
        self.root.update()
        return self.isRunning

    def killInterface(self):
        self.isRunning = False
