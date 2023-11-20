import pygame

class Musique:
    def __init__(self):
        self.music = pygame.mixer_music.load("west_coaster.wav")
        self.music_volume = pygame.mixer.music.set_volume(0.25)
        self.music_play = pygame.mixer.music.play(loops=-1)
        self.okay_lezgo = pygame.mixer.Sound("OKAY_LEZGOOO.wav")
        self.sound_volume()
    def sound_volume(self):
        self.okay_lezgo.set_volume(0.15)
        