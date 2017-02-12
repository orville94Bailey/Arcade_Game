import pygame

class Beat(pygame.sprite.Sprite):

    strength = 0.0
    startTime = 0.0
    endTime = 0.0

    def __init__(self, strength, startTime, endTime):
        super().__init__()

        self.strength = strength
        self.startTime = startTime
        self.endTime = endTime