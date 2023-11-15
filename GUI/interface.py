from tkinter import *

# On définit une classe "Interface" qui prend en argument deux dictionnaires,
# les variables et les fonctions donc l'interface a besoin pour s'implémenter

class Interface():
    def __init__(self, dico_variables, dico_functions):
        self.var = dico_variables
        self.func = dico_functions

        self.root = Tk()
        self.root.title("Bienvenue dans le Roller Coaster 3000, visiteur !")

        

