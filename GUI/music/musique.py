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
        self.music_volume = pygame.mixer.music.set_volume(0.20)
        self.music_play = pygame.mixer.music.play(loops=-1)
        self.okay_lezgo = pygame.mixer.Sound("GUI/music/OKAY_LEZGOOO.wav")
        self.sound_volume()

    def sound_volume(self):
        """
        methode pour régler le volume sonore
        """
        self.okay_lezgo.set_volume(0.15)
