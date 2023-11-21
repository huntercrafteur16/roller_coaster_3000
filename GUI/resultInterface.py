import matplotlib.pyplot as plt
import numpy as np


class ResultInterface():
    time: list

    def __init__(self, subplt_nbr, subplt_titles) -> None:
        self.subplt_nbr = subplt_nbr
        self.subplt_titles = subplt_titles

    def fill_time(self, time):
        self.time = time

    def _fill_datas_to_subplot(self, datas):
        self.fig, self.ax = plt.subplots(self.subplt_nbr, sharex=True)
        for i in range(self.subplt_nbr):
            self.ax[i].set_title(self.subplt_titles[i])
            self.ax[i].plot(self.time, datas[i])

    def show(self):
        self.fig.show()


# r_int = ResultInterface(3, ["1", "2", "3"])
# t = np.arange(0, 10, 1e-3)
# s1 = np.cos(t)
# s2 = np.sin(t)
# s3 = np.sin(2*t)
# r_int.fill_time(t)
# r_int._fill_datas_to_subplot(0, s1)
# r_int._fill_datas_to_subplot(1, s2)
# r_int._fill_datas_to_subplot(2, s3)
# r_int.show()
