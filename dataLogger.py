import numpy as np
from GUI.interface import Interface
from GUI.resultInterface import ResultInterface
from Physique.physicManager import physicManager


class dataLogger:
    time: list

    def __init__(self, manager: physicManager):
        self.result_render = ResultInterface(
            4, ["vitesse", "acceleration", "energie", "puissance"])
        self.manager = manager
        self.time = []
        self.datas = {"velocity": [],
                      "acceleration": [],
                      "potential_energie": [],
                      "kinetic_energie": [],
                      "meca_energie": [],
                      "electric_power": []}

    def record(self):

        wagon = self.manager.getWagon()
        self.time.append(self.manager.getTime())
        self.datas["velocity"].append(
            self.manager.getWagon().get_chassis_velocity()[0])
        self.datas["potential_energie"].append(wagon.get_potential())
        self.datas["kinetic_energie"].append(wagon.get_kinetic())
        self.datas["meca_energie"].append(wagon.get_total_energy())
        self.datas["electric_power"].append(wagon.get_puissance())

    def reset(self):
        self.time = []
        self.datas = {"velocity": [],
                      "acceleration": [],
                      "potential_energie": [],
                      "kinetic_energie": [],
                      "meca_energie": [],
                      "electric_power": []}

    def render_result(self):

        self.result_render.fill_time(self.time)
        self._compute_accel()
        self.result_render._fill_datas_to_subplot(
            [self.datas["velocity"], self.datas["acceleration"], self.datas["meca_energie"], self.datas["electric_power"]])
        self.result_render.show()

    def _compute_accel(self):
        self.datas["acceleration"] = [0]
        for i in range(len(self.time)-1):
            self.datas["acceleration"].append((self.datas["velocity"][i+1]-self.datas["velocity"]
                                               [i])/(self.time[i+1]-self.time[i]))
