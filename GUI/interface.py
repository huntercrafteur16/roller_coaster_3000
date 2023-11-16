from tkinter import *

from matplotlib.sankey import UP
from GUI.graphiques import graphe_vitesse, graphe_accel

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# On définit une classe "Interface" qui prend en argument deux dictionnaires,
# les variables et les fonctions donc l'interface a besoin pour s'implémenter


class Interface():
    def __init__(self, dico_variables, dico_functions):
        self.var = dico_variables
        self.func = dico_functions

        # Fenêtre principale
        self.root = Tk()
        self.root.title("Bienvenue dans le Roller Coaster 3000, visiteur !")

        # Deux frames : la barre d'outils et la simulation
        toolbar = Frame(self.root, bg="lightgray")
        simu = Frame(self.root, borderwidth=5, bg="white")
        toolbar.pack(side=TOP, expand=False, fill=X)
        simu.pack(side=BOTTOM, expand=True, fill=BOTH)

        # Variables
        m, v, f = DoubleVar(value=1), DoubleVar(value=1), DoubleVar(value=0.1)

        # Boutons Start/Reset
        buttons = Frame(toolbar, bg="lightgray", height=100, padx=5)
        buttons.grid(row=0, column=0)

        def doNothing():
            pass

        start_reset = Button(buttons, command=doNothing, width=10, height=2,
                             text='Start/Reset', fg='#30b000', activebackground='#30b000')
        play_pause = Button(buttons, command=doNothing, width=10, height=2,
                            text='Play/Pause', fg='#0080ff', activebackground='#0080ff')
        start_reset.grid(row=0, column=0, padx=3, pady=3)
        play_pause.grid(row=0, column=1, padx=3, pady=3)

        # Paramètres
        param = Frame(toolbar, bg="lightgray", width=200, padx=5, pady=5)
        param.grid(row=0, column=1)

        apply_param = Button(param, height=2, text='Appliquer les paramètres',
                             bg='lightgray', fg='red', activebackground='red', command=doNothing)
        apply_param.grid(row=0, column=0, padx=5, pady=5)

        # masse
        param_m = Frame(param)
        label_m = Label(param_m, text='Masse du wagon (kg)',
                        width=20, height=1)
        entry_m = Entry(param_m, textvariable=m, width=5)
        scale_m = Scale(param_m, from_=0, to=100, showvalue=False, variable=m,
                        tickinterval=25, orient=HORIZONTAL, width=10)
        # vitesse
        param_v = Frame(param)
        label_v = Label(param_v, text='Vitesse des treuils (m/s)',
                        width=20, height=1)
        entry_v = Entry(param_v, textvariable=v, width=5)
        scale_v = Scale(param_v, from_=0, to=100, showvalue=False, variable=v,
                        tickinterval=25, orient=HORIZONTAL, width=10)
        # coef de frottement
        param_f = Frame(param)
        label_f = Label(param_f, text='Coef. de frottement (kg/m)',
                        width=20, height=1)
        entry_f = Entry(param_f, textvariable=f, width=5)
        scale_f = Scale(param_f, from_=0, to=10, showvalue=False, variable=f,
                        tickinterval=2, orient=HORIZONTAL, width=10)

        label_m.grid(row=0, column=1, columnspan=2)
        entry_m.grid(row=1, column=1, padx=3)
        scale_m.grid(row=1, column=2)
        param_m.grid(row=0, column=1, padx=5, pady=5)

        label_v.grid(row=0, column=1, columnspan=2)
        entry_v.grid(row=1, column=1, padx=3)
        scale_v.grid(row=1, column=2)
        param_v.grid(row=0, column=2, padx=5, pady=5)

        label_f.grid(row=0, column=1, columnspan=2)
        entry_f.grid(row=1, column=1, padx=3)
        scale_f.grid(row=1, column=2)
        param_f.grid(row=0, column=3, padx=5, pady=5)

        # A l'intérieur de simu : roller coaster et graphe

        roller_coaster = Frame(simu, bg='white')
        frame_graph = Frame(simu)
        roller_coaster.grid(row=1, column=1, rowspan=3, columnspan=3)

        # Boutons radio pour voir ou non un des graphes proposés
        void = Frame(toolbar, width=15, bg="lightgray", padx=5)
        graph_choice = Frame(toolbar, padx=5)
        void.grid(row=0, column=2)
        graph_choice.grid(row=0, column=3)

        choice = IntVar(value=0)
        label_graph_choice = Label(
            graph_choice, text="Choix du graphe à afficher")
        label_graph_choice.pack(side=TOP)

        Radiobuttons = Frame(graph_choice)
        Radiobuttons.pack(side=BOTTOM)

        # Fonctions des boutons qui réalisent les graphes matplotlib
        List_speeds, List_accels = self.var['List_speeds'], self.var['List_accels']
        t_graph = DoubleVar(value=10)
        # empty_graph = plt.figure()
        # graph = FigureCanvasTkAgg(empty_graph, master=frame_graph)

        # def renderNothing():
        #    for widget in frame_graph.winfo_children():
        #        widget.destroy()
        #    pass

        # def renderSpeeds():
        #    for widget in frame_graph.winfo_children():
        #        widget.destroy()
        #    graph.figure = graphe_vitesse(List_speeds, t_graph.get())
        #    canvas = graph.get_tk_widget()
        #    canvas.pack()
        #    frame_graph.grid(row=0, column=3, sticky=E)

        # def renderAccels():
        #    for widget in frame_graph.winfo_children():
        #        widget.destroy()
        #    graph.figure = graphe_accel(List_accels, t_graph.get())
        #    canvas = graph.get_tk_widget()
        #    canvas.pack()
        #    frame_graph.grid(row=0, column=3, sticky=E)

        Radiobutton(Radiobuttons, variable=choice, value=1,
                    height=1, command=doNothing).grid(row=1, column=0)
        Label(Radiobuttons, text='aucun', width=4,
              height=1).grid(row=1, column=1)
        Label(Radiobuttons, text=' ', width=3, height=1).grid(row=1, column=2)
        Radiobutton(Radiobuttons, variable=choice, value=2,
                    height=1, command=doNothing).grid(row=1, column=3)
        Label(Radiobuttons, text='vitesse(t)',
              width=6, height=1).grid(row=1, column=4)
        Label(Radiobuttons, text=' ', width=3, height=1).grid(row=1, column=5)
        Radiobutton(Radiobuttons, variable=choice, value=3,
                    height=1, command=doNothing).grid(row=1, column=6)
        Label(Radiobuttons, text='accélération(t)',
              width=10, height=1).grid(row=1, column=7)
        Label(Radiobuttons, text=' ', width=3, height=1).grid(row=1, column=8)

        Label(Radiobuttons, text='Durée (s): ', width=7,
              height=1).grid(row=1, column=9, sticky=E)
        Entry(Radiobuttons, textvariable=t_graph, width=4).grid(
            row=1, column=10, sticky=E, padx=5, pady=5)

    def renderGUI(self):
        self.root.mainloop()
