import pygame
import math
from src.utils.asset_loader import load_image

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20, amplitude=20, speed=2, phase=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = load_image("level_3/platform.png", size=(width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.initial_y = y
        self.amplitude = amplitude
        self.speed = speed
        self.phase = phase  
        self.timer = 0

    def update(self):
        self.timer += self.speed
        offset = math.sin(math.radians(self.timer + self.phase)) * self.amplitude
        self.rect.y = self.initial_y + offset
