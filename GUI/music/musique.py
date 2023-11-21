import pygame


class Musique:
    def __init__(self):
        pygame.mixer.init()
        self.music = pygame.mixer.music.load("GUI/music/west_coaster.mp3")
        self.music_volume = pygame.mixer.music.set_volume(0.20)
        self.music_play = pygame.mixer.music.play(loops=-1)
        self.okay_lezgo = pygame.mixer.Sound("GUI/music/OKAY_LEZGOOO.wav")
        self.sound_volume()

    def sound_volume(self):
        self.okay_lezgo.set_volume(0.15)
