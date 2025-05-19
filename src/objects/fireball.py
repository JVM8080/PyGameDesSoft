import pygame
import random
from config import HEIGHT, WIDTH

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # cuadrado rojo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = HEIGHT + 20  
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y -= self.speed  
        if self.rect.bottom < 0:
            self.kill()