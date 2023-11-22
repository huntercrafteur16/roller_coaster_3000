"""
Module qui gère l'interface
"""

from tkinter import N, X, Frame, Button, Tk, DoubleVar, BOTTOM, TOP
from tkinter import BOTH, IntVar, Entry, Scale, Label, HORIZONTAL
from typing import Callable
from GUI.music.musique import Musique
import sys
import subprocess

# On définit une classe "Interface" qui prend en argument deux dictionnaires,
# les variables et les fonctions donc l'interface a besoin pour s'implémenter


class Interface():
    """
    Classe interface pour l'affichage GUI
    """
    play_pause_button_function: Callable
    start_reset_button_function: Callable
    apply_button_function: Callable
    open_file_function: Callable
    show_results: Callable

    isRunning: bool

    def __init__(self, button_functions: dict):
        self.start_reset_button_function = button_functions["start_reset"]
        self.play_pause_button_function = button_functions["play_pause"]
        self.apply_button_function = button_functions["apply"]
        self.open_file_function = button_functions["open"]
        self.show_results = button_functions["show_results"]
        # dimensions de la fenetre pymunk en px
        roller_coaster_width = 1900
        roller_coaster_height = 700
        # Fenêtre principale
        self.root = Tk()
        self.root.title("Bienvenue dans le Roller Coaster 3000, visiteur !")
        self.root.state('zoomed')
        self.isRunning = True
        self.root.protocol('WM_DELETE_WINDOW', self.killInterface)
        # Trois frames : barre d'outils, simulation, barre des graphes
        toolbar = Frame(self.root, bg="lightgray")
        simu = Frame(self.root, borderwidth=5, bg="white")
        self.simu = simu
        self.graphbar = Frame(self.root, bg="lightgray")

        toolbar.pack(side=TOP, expand=False, fill=X)
        simu.pack(anchor=N, expand=True, fill=BOTH, padx=5)
        self.graphbar.pack(side=BOTTOM, fill=X, expand=True, padx=5, pady=5)

        # Variables
        self.applied_m, self.applied_f, self.applied_v = 1000, 100000, 50
        self.applied_nbr_wagon, self.applied_c = 3, 0.001
        m = DoubleVar(value=1)
        f = DoubleVar(value=100)
        nbr_wagon = IntVar(value=3)
        v = DoubleVar(value=5)
        c = DoubleVar(value=1)

        # Musique
        self.music = Musique()

        def apply_values():
            self.applied_m = float(m.get())*1000
            self.applied_f = float(f.get())*1000
            self.applied_v = float(v.get())*10
            self.applied_nbr_wagon = int(nbr_wagon.get())
            self.applied_c = float(c.get())*0.001
            self.apply_button_function()
            print("nouvelles valeurs")
        # Boutons Start/Reset

        buttons = Frame(toolbar, bg="lightgray", height=100, padx=5)
        buttons.grid(row=0, column=0)

        self.start_reset = Button(buttons, command=self.start_reset_button_function,
                                  width=10, height=2, text='Start/Reset',
                                  fg='#30b000', activebackground='#30b000')
        self.play_pause = Button(buttons, command=self.play_pause_button_function,
                                 width=10, height=2, text='Play/Pause', fg='#0080ff',
                                 activebackground='#0080ff')
        self.start_reset.grid(row=0, column=0, padx=3, pady=3)
        self.play_pause.grid(row=0, column=1, padx=3, pady=3)
        open_filebutton = Button(buttons, command=self.open_file_function, width=10, height=2,
                                 text='Ouvrir tracé', fg='#000000', activebackground='#000000')
        open_filebutton.grid(row=0, column=2, padx=3, pady=3)

        show_result_button = Button(buttons, command=self.show_results, width=10, height=2,
                                    text='Afficher résult.', fg='#d08000',
                                    activebackground='#d08000')
        show_result_button.grid(row=0, column=3, padx=3, pady=3)
<<<<<<< Updated upstream
        # open_editor_button = Button(toolbar, command=self.open_editor, width=10, height=2,
        #                             text="Ouvrir éditeur", fg="#6400c8", activebackground="#6400c8")
        # open_editor_button.grid(row=0, column=4, padx=3, pady=3)
=======
>>>>>>> Stashed changes

        # Paramètres
        param = Frame(toolbar, bg="lightgray", width=200, padx=5, pady=5)
        param.grid(row=0, column=1)

        apply_param = Button(param, height=2, text='Appliquer les paramètres',
                             bg='lightgray', fg='red', activebackground='red', command=apply_values)
        apply_param.grid(row=0, column=0, padx=5, pady=5)

        # masse
        param_m = Frame(param)
        label_m = Label(param_m, text='Masse des wagons (Tonnes)',
                        width=25, height=1)
        entry_m = Entry(param_m, textvariable=m, width=5)
        scale_m = Scale(param_m, from_=1, to=50, showvalue=False, variable=m,
                        tickinterval=25, orient=HORIZONTAL, width=10)
        # force des propulseurs
        param_F = Frame(param)
        label_F = Label(param_F, text='Force des propulseurs (kN)',
                        width=25, height=1)
        entry_F = Entry(param_F, textvariable=f, width=5)
        scale_F = Scale(param_F, from_=50, to=1000, showvalue=False, variable=f,
                        tickinterval=500, orient=HORIZONTAL, width=10)
        # vitesse des treuils
        param_v = Frame(param)
        label_v = Label(param_v, text='Vitesse des treuils (m/s)',
                        width=25, height=1)
        entry_v = Entry(
            param_v, textvariable=v, width=5)
        scale_v = Scale(param_v, from_=1, to=10, showvalue=False,
                        variable=v, tickinterval=3, orient=HORIZONTAL, width=10)
        # nombre de wagons
        param_nbr_wagon = Frame(param)
        label_nbr_wagon = Label(param_nbr_wagon, text='Nombre de wagons',
                                width=25, height=1)
        entry_nbr_wagon = Entry(
            param_nbr_wagon, textvariable=nbr_wagon, width=5)
        scale_nbr_wagon = Scale(param_nbr_wagon, from_=0, to=10, showvalue=False,
                                variable=nbr_wagon, tickinterval=2, orient=HORIZONTAL, width=10)
        # coefficient de frottement
        param_c = Frame(param)
        label_c = Label(param_c, text='Coef. de frott. (arb.)',
                        width=25, height=1)
        entry_c = Entry(
            param_c, textvariable=c, width=5)
        scale_c = Scale(param_c, from_=0, to=10, showvalue=False,
                        variable=c, tickinterval=2, orient=HORIZONTAL, width=10)

        # On affiche tout
        label_m.grid(row=0, column=1, columnspan=2)
        entry_m.grid(row=1, column=1, padx=3)
        scale_m.grid(row=1, column=2)
        param_m.grid(row=0, column=1, padx=10, pady=5)

        label_F.grid(row=0, column=1, columnspan=2)
        entry_F.grid(row=1, column=1, padx=3)
        scale_F.grid(row=1, column=2)
        param_F.grid(row=0, column=2, padx=10, pady=5)

        label_v.grid(row=0, column=1, columnspan=2)
        entry_v.grid(row=1, column=1, padx=3)
        scale_v.grid(row=1, column=2)
        param_v.grid(row=0, column=3, padx=10, pady=5)

        label_nbr_wagon.grid(row=0, column=1, columnspan=2)
        entry_nbr_wagon.grid(row=1, column=1, padx=3)
        scale_nbr_wagon.grid(row=1, column=2)
        param_nbr_wagon.grid(row=0, column=4, padx=10, pady=5)

        label_c.grid(row=0, column=1, columnspan=2)
        entry_c.grid(row=1, column=1, padx=3)
        scale_c.grid(row=1, column=2)
        param_c.grid(row=0, column=5, padx=10, pady=5)

        # A l'intérieur de simu : roller coaster et graphe
        self.roller_coaster = Frame(
            simu, bg='white', height=roller_coaster_height, width=roller_coaster_width)
        self.frame_graph = Frame(
            self.graphbar, width=1800, height=50, bg="lightgray")
        Vitesse = Label(self.frame_graph, text="Vitesse",
                        justify="center", bg="lightgray", width="20")
        Vitesse.grid(row=0, column=1, sticky="nsew", padx=400)

        Energie = Label(self.frame_graph, text="Energie",
                        justify="center", bg="lightgray", width="20")
        Energie.grid(row=0, column=0, sticky="nsew", padx=400)
        self.frame_graph.pack(expand=1)
        self.roller_coaster.grid(
            row=1, column=1, rowspan=3, columnspan=3, sticky=N)

    # Donne la frame qui doit contenir un graphe et le choix de graphe associé
    def get_graph_frame(self):
        """return self.graphbar"""
        return self.graphbar

    # Donne la frame dans laquelle
    def get_pymunk_frame(self):
        "retourne le frame contenant la simulation physique pymunk"
        return self.roller_coaster

    # Rend les valeurs choisies
    def get_param(self):
        """renvoie les paramètres des boutons modifiant le comportement
        - 'mass'
        - 'force'
        - 'v_treuil'
        - 'nbr_wagon'
        - 'coef_frot'
        """
        return {'mass': self.applied_m, 'F_prop': self.applied_f, 'v_treuil': self.applied_v,
                'nbr_wagon': self.applied_nbr_wagon, 'coef_frot': self.applied_c}

    def render_GUI(self) -> bool:
        """met à jour l'interface"""
        self.root.update()
        return self.isRunning

    def killInterface(self):
        """arrete l'interface """
        self.isRunning = False
