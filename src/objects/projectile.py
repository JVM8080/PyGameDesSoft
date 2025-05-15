import pygame
from config import SOUND_VOLUME_SFX
from pygame import mixer
from src.utils.asset_loader import load_image
from config import HEIGHT,WIDTH

PROJECTILE_SOUND = None
ENERGYBALL_SOUND = None

class Projectile:
    def __init__(self, x, y, direction, play_sound=True):
        global PROJECTILE_SOUND
        if PROJECTILE_SOUND is None:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            PROJECTILE_SOUND = pygame.mixer.Sound("assets/sounds/dipper-attack1.ogg")

        if play_sound:
            PROJECTILE_SOUND.set_volume(SOUND_VOLUME_SFX)
            PROJECTILE_SOUND.play()
            
        self.sprite_sheet = load_image("dipper/dipper_attack1.png", size=(80*5, 80))
        self.frames = []
        self.frame_count = 5
        self.frame_width = self.sprite_sheet.get_width() // self.frame_count
        self.frame_height = self.sprite_sheet.get_height()

        for i in range(self.frame_count):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            self.frames.append(frame)

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_interval = 5

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 8
        self.damage = 2
        self.direction = direction
        self.lifetime = 60

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        self.frame_timer += 1
        if self.frame_timer >= self.frame_interval:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        return (self.rect.right < 0 or self.rect.left > 800 or
                self.rect.bottom < 0 or self.rect.top > 600)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class EnergyBall(Projectile):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, play_sound=False)  

        global ENERGYBALL_SOUND
        if ENERGYBALL_SOUND is None:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            ENERGYBALL_SOUND = pygame.mixer.Sound("assets/sounds/dipper-attack2.wav")

        ENERGYBALL_SOUND.set_volume(SOUND_VOLUME_SFX)
        ENERGYBALL_SOUND.play()



        self.sprite_sheet = load_image("dipper/dipper_attack2.png", size=(50*5, 50))

        self.frames = []
        frame_width = self.sprite_sheet.get_width() // 5
        frame_height = self.sprite_sheet.get_height()

        for i in range(5):
            frame = self.sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_interval = 5

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 4
        self.lifetime = 90
        self.damage = 4

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        self.frame_timer += 1
        if self.frame_timer >= self.frame_interval:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        return (self.rect.right < 0 or self.rect.left > 800 or
                self.rect.bottom < 0 or self.rect.top > 600)
