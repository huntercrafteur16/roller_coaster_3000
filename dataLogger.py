"""
Module permettant l'affichage des résultats à la fin de la simulation
"""
from GUI.resultInterface import ResultInterface
import Physique.physicManager


class dataLogger:
    """
    Classe dataLogger pour gérer l'affichage des graphes à la fin de la simualtion
    """
    time: list

    def __init__(self):
        self.result_render = ResultInterface(
            4, ["vitesse en m/s", "acceleration en g", "énergie en J", "puissance électrique installation en W"])
        self.manager = None
        self.time = []
        self.datas = {"velocity": [],
                      "acceleration": [],
                      "potential_energie": [],
                      "kinetic_energie": [],
                      "meca_energie": [],
                      "electric_power": []}

    def setManager(self, manager: Physique.physicManager.physicManager):
        """set the manager the logger should get data from """
        self.manager = manager

    def record(self):
        """
        Lit les valeurs à ajouter dans les graphes et les garde dans les listes correspondantes
        """
        wagon = self.manager.getWagon()
        self.time.append(self.manager.getTime())
        L = self.manager.train.liste_wagon
        total_energy = 0
        potential_energy = 0
        kinetic_energy = 0
        for wagon in L:
            potential_energy += wagon.get_potential()
            kinetic_energy += wagon.get_kinetic()
            total_energy = kinetic_energy + potential_energy
        self.datas["velocity"].append(
            self.manager.getWagon().get_chassis_velocity()[0]/Physique.physicManager.physicManager.ppm)
        self.datas["potential_energie"].append(potential_energy)
        self.datas["kinetic_energie"].append(kinetic_energy)
        self.datas["meca_energie"].append(total_energy)
        self.datas["electric_power"].append(self.manager.power)

    def reset(self):
        """
        Réinitialise les listes contenant les données
        """
        self.time = []
        self.datas = {"velocity": [],
                      "acceleration": [],
                      "potential_energie": [],
                      "kinetic_energie": [],
                      "meca_energie": [],
                      "electric_power": []}

    def render_result(self):
        """
        Renvoie les résultats
        """
        self.result_render.fill_time(self.time)
        self._compute_accel()

        self.result_render.fill_datas_to_subplot(
            [self.datas["velocity"], self.datas["acceleration"],
             self.datas["meca_energie"], self.datas["electric_power"]])
        self.result_render.show()

    def _compute_accel(self):
        """
        Calcule l'accélération en dérivant terme à terme
        """
        self.datas["acceleration"] = [0]
        for i in range(len(self.time)-1):

            accel = (self.datas["velocity"][i+1]-self.datas["velocity"]
                     [i])/(self.time[i+1]-self.time[i])
            self.datas["acceleration"].append(
                accel/9.81)
