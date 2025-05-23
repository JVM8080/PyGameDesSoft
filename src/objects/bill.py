import pygame
import math
from src.utils.asset_loader import load_image

class Bill(pygame.sprite.Sprite):
    def __init__(self, x, y, phase=0):
        super().__init__()

        full_image_normal = load_image("level_3/bill_1.png", size=(75 * 3, 75))
        self.frames_normal = []
        for i in range(3):
            frame = pygame.Surface((75, 75), pygame.SRCALPHA)
            frame.blit(full_image_normal, (0, 0), (i * 75, 0, 75, 75))
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames_normal.append(frame)

        full_image_damaged = load_image("level_3/bill_2.png", size=(75 * 3, 75))
        self.frames_damaged = []
        for i in range(3):
            frame = pygame.Surface((75, 75), pygame.SRCALPHA)
            frame.blit(full_image_damaged, (0, 0), (i * 75, 0, 75, 75))
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames_damaged.append(frame)

        self.frames = self.frames_normal  

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150

        self.base_x = x
        self.base_y = y
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(self.base_x, self.base_y))

        self.oscillation_amplitude = 20
        self.oscillation_speed = 0.005
        self.phase = math.radians(phase)

        self.health = 200
        self.max_health = 200
        self.total_time = 0
        
        self.is_damaged = False

    def update(self, dt, player_rect=None):
        self.total_time += dt

        if self.health <= 0:
            self.kill()
            return  

        if self.health < 120 and not self.is_damaged:
            self.frames = self.frames_damaged
            self.is_damaged = True  
        elif self.health >= 120 and self.is_damaged:
            self.frames = self.frames_normal
            self.is_damaged = False  


        offset = self.oscillation_amplitude * math.sin(self.total_time * self.oscillation_speed + self.phase)
        self.rect.centery = self.base_y + offset

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

