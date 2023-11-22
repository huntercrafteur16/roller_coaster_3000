"""
Module de test du fichier physicmanager
"""
from physicManager import physicManager
import pygame
manager = physicManager(1000, 600)

cont = True
while cont == True:
    cont = manager.process()
