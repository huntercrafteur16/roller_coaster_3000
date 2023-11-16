from physicManager import *
import pygame
manager = physicManager(1000, 600)

cont = True
while cont == True:
    cont = manager.process()
