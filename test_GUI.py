from GUI.interface import *
from GUI.graphiques import AnimatedGraph
import time

GUI = Interface()
GUI.render_GUI()

while True:
    print(GUI.get_param())
    time.sleep(1/60)
    GUI.render_GUI()
