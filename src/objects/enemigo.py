import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=4):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0))  # Cubo negro
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = 2

    def update(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = max((dx**2 + dy**2) ** 0.5, 1)
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)

