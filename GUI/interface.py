from tkinter import *

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
        buttons.pack(side=LEFT, expand=True, fill=X)

        def doNothing():
            pass

        start_reset = Button(buttons, command=doNothing, width=10, height=2,
                             text='Start/Reset', fg='#30b000', activebackground='#30b000')
        play_pause = Button(buttons, command=doNothing, width=10, height=2,
                            text='Play/Pause', fg='#0080ff', activebackground='#0080ff')
        start_reset.grid(row=0, column=0, padx=3, pady=3)
        play_pause.grid(row=0, column=1, padx=3, pady=3)

        # Paramètres
        param = Frame(toolbar, bg="lightgray", width=200, padx=5)
        param.pack(side=RIGHT, expand=False)

        apply_param = Button(param, height=2, text='Appliquer les paramètres',
                             bg='lightgray', fg='red', activebackground='red', command=doNothing)
        apply_param.grid(row=0, column=0, padx=5, pady=5)

        param_m = Frame(param)
        label_m = Label(param_m, text='Masse du wagon (kg)',
                        width=20, height=1)
        entry_m = Entry(param_m, textvariable=m, width=5)
        scale_m = Scale(param_m, from_=0, to=100, showvalue=False, variable=m,
                        tickinterval=25, orient=HORIZONTAL, width=10)

        param_v = Frame(param)
        label_v = Label(param_v, text='Vitesse des treuils (m/s)',
                        width=20, height=1)
        entry_v = Entry(param_v, textvariable=v, width=5)
        scale_v = Scale(param_v, from_=0, to=100, showvalue=False, variable=v,
                        tickinterval=25, orient=HORIZONTAL, width=10)

        param_f = Frame(param)
        label_f = Label(param_f, text='Coef. de frottement (kg/m)',
                        width=20, height=1)
        entry_f = Entry(param_f, textvariable=f, width=5)
        scale_f = Scale(param_f, from_=0, to=10, showvalue=False, variable=f,
                        tickinterval=2, orient=HORIZONTAL, width=10)

        label_m.grid(row=0, column=1)
        entry_m.grid(row=0, column=2)
        scale_m.grid(row=0, column=3)
        param_m.grid(row=0, column=1, padx=5, pady=5)

        label_v.grid(row=0, column=1)
        entry_v.grid(row=0, column=2)
        scale_v.grid(row=0, column=3)
        param_v.grid(row=0, column=2, padx=5, pady=5)

        label_f.grid(row=0, column=1)
        entry_f.grid(row=0, column=2)
        scale_f.grid(row=0, column=3)
        param_f.grid(row=0, column=3, padx=5, pady=5)

    def renderGUI(self):
        self.root.mainloop()
