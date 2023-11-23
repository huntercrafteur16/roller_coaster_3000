"""
Definition de la classe ResultInterface et methodes
"""

import matplotlib.pyplot as plt


class ResultInterface():
    """
    Classe permetant l'affichage de la fenetre des resultats
    """
    time: list

    def __init__(self, subplt_nbr, subplt_titles) -> None:
        self.subplt_nbr = subplt_nbr
        self.subplt_titles = subplt_titles

    def fill_time(self, time):
        """ajoute l'attribut temps"""
        self.time = time

    def fill_datas_to_subplot(self, datas: list):
        """
        remplit les listes de données à afficher
        """

        self.fig, self.ax = plt.subplots(self.subplt_nbr, sharex=True)

        for i in range(self.subplt_nbr):
            self.ax[i].set_title(self.subplt_titles[i])

            self.ax[i].plot(self.time[1::], datas[i][1::])

    def show(self):
        """
        affiche les graphes
        """
        self.fig.show()
