import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer

JUMP_SOUND = None

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND
        self.image = load_image("player.png", size=(40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.speed = 1
        self.jump_force = -8
        self.gravity = 0.3
        self.on_ground = False
        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.mp3")

    def update(self, keys):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()

        self.vel_y += self.gravity
        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
