"""
ajoute la musique à la fenetre
"""
import pygame


class Musique:
    """
    Classe permettant l'ajout de la musique
    """

    def __init__(self):
        pygame.mixer.init()
        self.music = pygame.mixer.music.load("GUI/music/west_coaster.mp3")
        self.etat = 1
        self.music_volume = pygame.mixer.music.set_volume(0.20)
        self.okay_lezgo = pygame.mixer.Sound("GUI/music/OKAY_LEZGOOO.wav")
        self.sound_volume()

    def sound_volume(self):
        """
        methode pour ajouter potentielement un son
        """
        self.okay_lezgo.set_volume(0.15)
        
    def music_mute(self):
        """
        methode pour lancer la musique de fond ou l'arreter
        """
        if self.etat==1:
            self.music_volume = pygame.mixer.music.play(loops=-1)
            self.etat=0
        else:
            self.music_volume = pygame.mixer.music.stop()
            self.etat=1

