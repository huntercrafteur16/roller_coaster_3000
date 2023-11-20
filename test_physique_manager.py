from Physique.physicManager import *

import pygame
manager = physicManager(1000, 600)
manager.play()
cont = True
while cont == True:
    cont = manager.process()
