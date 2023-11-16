from physicManager import *
import pygame
manager = physicManager(600, 600)

cont = True
while cont == True:
    cont = manager.process()
