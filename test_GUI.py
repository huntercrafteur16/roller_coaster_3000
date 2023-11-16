from GUI.interface import *
from GUI.graphiques import *

var = {}
func = {}
List_speeds = [1, 3, 5, 8, 14, 12, 5, 4, 6, 9, 9, 8, 5, 4, 2]
List_accels = [1, 2, 1, 5, 7, 11, 17, 18, 18, 17, 14, 8, 5, 4, 2]
var['List_speeds'] = List_speeds
var['List_accels'] = List_accels

GUI = Interface(var, func)
GUI.renderGUI()
