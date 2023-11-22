"""
Module de test du fichier physicmanager
"""
from physicManager import physicManager
manager = physicManager(1000, 600)

cont = True
while cont is True:
    cont = manager.process()
