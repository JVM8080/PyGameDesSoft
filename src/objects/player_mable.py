import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer
from src.objects.power import PoderBase

JUMP_SOUND = None

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND

        self.image_idle = load_image("mabel/mabel.png").convert_alpha()
        self.anim_left = load_image('mabel/mabel indo pra esquerda.png').convert_alpha()
        self.anim_right = load_image('mabel/mabel pra direita.png').convert_alpha()

        # Cálculo correto para cada spritesheet
        frame_width_left = self.anim_left.get_width() // 3
        frame_height_left = self.anim_left.get_height()

        frame_width_right = self.anim_right.get_width() // 3
        frame_height_right = self.anim_right.get_height()

        self.mabel_anim_left = []
        for i in range(3):
            frame = self.anim_left.subsurface(pygame.Rect(i * frame_width_left, 0, frame_width_left, frame_height_left))
            self.mabel_anim_left.append(frame)

        self.mabel_anim_right = []
        for i in range(3):
            frame = self.anim_right.subsurface(pygame.Rect(i * frame_width_right, 0, frame_width_right, frame_height_right))
            self.mabel_anim_right.append(frame)

        self.frame_left = 0
        self.frame_right = 0

        self.image = self.mabel_anim_right[self.frame_right]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.speed = 1
        self.jump_force = -8
        self.gravity = 0.3
        self.on_ground = False

        self.poder_group = pygame.sprite.Group()
        self.moeda_spritesheet = load_image("stan/poder moedas.png").convert_alpha()

        self.moeda_frame_width = self.moeda_spritesheet.get_width() // 6
        self.moeda_frame_height = self.moeda_spritesheet.get_height()

        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.mp3")

        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50

        self.z_pressed_last_frame = False

    def update(self, keys):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        dx = 0

        if keys[pygame.K_z] and not self.z_pressed_last_frame:
            direction = 1 if keys[pygame.K_RIGHT] else -1
            moeda = PoderBase(
                self.rect.centerx,
                self.rect.centery,
                direction,
                self.moeda_spritesheet,
                frame_count=6,
                frame_width=self.moeda_frame_width,
                frame_height=self.moeda_frame_height
            )
            self.poder_group.add(moeda)

        self.z_pressed_last_frame = keys[pygame.K_z]

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_left = (self.frame_left + 1) % len(self.mabel_anim_left)
                self.image = self.mabel_anim_left[self.frame_left]

        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_right = (self.frame_right + 1) % len(self.mabel_anim_right)
                self.image = self.mabel_anim_right[self.frame_right]
        
        else:
            self.image = self.image_idle

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

        self.poder_group.update()

    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.poder_group.draw(screen)
