"""
Module permettant l'affichage des résultats à la fin de la simulation
"""
from GUI.resultInterface import ResultInterface
from Physique.physicManager import physicManager


class dataLogger:
    """
    Classe dataLogger pour gérer l'affichage des graphes à la fin de la simualtion
    """
    time: list

    def __init__(self):
        self.result_render = ResultInterface(
            4, ["vitesse", "acceleration", "energie", "puissance"])
        self.manager = None
        self.time = []
        self.datas = {"velocity": [],
                      "acceleration": [],
                      "potential_energie": [],
                      "kinetic_energie": [],
                      "meca_energie": [],
                      "electric_power": []}

    def setManager(self, manager):
        self.manager = manager

    def record(self):
        """
        Lit les valeurs à ajouter dans les graphes et les garde dans les listes correspondantes
        """
        wagon = self.manager.getWagon()
        self.time.append(self.manager.getTime())
        L = self.manager.Train.liste_wagon
        total_energy = 0
        potential_energy = 0
        kinetic_energy = 0
        for wagon in L:
            potential_energy += wagon.get_potential()
            kinetic_energy += wagon.get_kinetic()
            total_energy = kinetic_energy + potential_energy
        self.datas["velocity"].append(
            self.manager.getWagon().get_chassis_velocity()[0])
        self.datas["potential_energie"].append(potential_energy)
        self.datas["kinetic_energie"].append(kinetic_energy)
        self.datas["meca_energie"].append(total_energy)
        self.datas["electric_power"].append(wagon.get_puissance())

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
        self.result_render._fill_datas_to_subplot(
            [self.datas["velocity"], self.datas["acceleration"],
             self.datas["meca_energie"], self.datas["electric_power"]])
        self.result_render.show()

    def _compute_accel(self):
        """
        Calcule l'accélération
        """
        self.datas["acceleration"] = [0]
        for i in range(len(self.time)-1):
            try:
                self.datas["acceleration"].append((self.datas["velocity"][i+1]-self.datas["velocity"]
                                                   [i])/(self.time[i+1]-self.time[i]))
            except:
                print(self.time)
