import pygame
from src.utils.asset_loader import load_image

class Obstacle:
    def __init__(self, x, y):
        self.image = load_image("obstacle.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
