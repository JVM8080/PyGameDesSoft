import pygame
import math

class Projectile:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.direction = direction
        self.lifetime = 60

    def update(self):        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        return (self.rect.right < 0 or self.rect.left > 800 or
                self.rect.bottom < 0 or self.rect.top > 600)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class EnergyBall(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 200, 255), (10, 10), 10)  # Bola azul
        self.speed = 5
        self.lifetime = 90
        self.damage = 2  
