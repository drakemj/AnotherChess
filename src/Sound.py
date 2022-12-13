import pygame

class SoundMixer:
    sounds = []

    def __init__(self):
        self.sounds.append(pygame.mixer.Sound("src/assets/sounds/capture.mp3"))
        self.sounds.append(pygame.mixer.Sound("src/assets/sounds/move-self.mp3"))

    def playCapture(self):
        self.sounds[0].play()

    def playMove(self):
        self.sounds[1].play()