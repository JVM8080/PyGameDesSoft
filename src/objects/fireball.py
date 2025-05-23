import pygame
import random
from config import HEIGHT, WIDTH
from src.utils.asset_loader import load_image

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Cargar el spritesheet completo (250x50 si cada frame es 50x50 y hay 5 frames en fila)
        spritesheet = load_image("level_3/chuva.png", size=(50 * 5, 50))

        # Tamaño de cada frame
        frame_width = spritesheet.get_width() // 5
        frame_height = spritesheet.get_height()

        # Extraer los 5 frames (horizontalmente)
        self.frames = []
        for i in range(5):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # milisegundos

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = HEIGHT + 20
        self.speed = random.randint(3, 6)

        self.last_update = pygame.time.get_ticks()

    def update(self):
        # Control de tiempo para animación
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Movimiento hacia arriba
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
