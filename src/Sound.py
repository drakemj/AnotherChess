import pygame

class SoundMixer:
    sounds = []

    def __init__(self):
        self.sounds.append(pygame.mixer.Sound("src/assets/sounds/capture.wav"))
        self.sounds.append(pygame.mixer.Sound("src/assets/sounds/move-self.wav"))
        self.sounds.append(pygame.mixer.Sound("src/assets/sounds/check.wav"))

    def playMove(self, capture, check):
        if check:
            self.sounds[2].play()
        elif capture:
            self.sounds[0].play()
        else:
            self.sounds[1].play()