import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer
from src.objects.power import PoderBase

JUMP_SOUND = None

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND

        self.image_idle = load_image("mabel/mabel.png", size=(60, "auto"))
        self.anim_left = load_image('mabel/mabel indo pra esquerda.png').convert_alpha()
        self.anim_right = load_image('mabel/mabel pra direita.png').convert_alpha()

        frame_width_left = self.anim_left.get_width() // 3
        frame_height_left = self.anim_left.get_height()
        self.mabel_anim_left = [
            self.anim_left.subsurface(pygame.Rect(i * frame_width_left, 0, frame_width_left, frame_height_left))
            for i in range(3)
        ]

        frame_width_right = self.anim_right.get_width() // 3
        frame_height_right = self.anim_right.get_height()
        self.mabel_anim_right = [
            self.anim_right.subsurface(pygame.Rect(i * frame_width_right, 0, frame_width_right, frame_height_right))
            for i in range(3)
        ]

        self.frame_left = 0
        self.frame_right = 0
        self.image = self.mabel_anim_right[self.frame_right]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.last_direction = 1
        self.vel_y = 0
        self.speed = 4
        self.jump_force = -13         
        self.gravity = 0.45            
        self.max_fall_speed = 10      
        self.on_ground = False

        self.poder_group = pygame.sprite.Group()
        estrela_original = load_image("mabel/estrela_poder_transparente.png").convert_alpha()

        reduzida_w = estrela_original.get_width() // 25
        reduzida_h = estrela_original.get_height() // 25
        self.estrela_direita = pygame.transform.scale(estrela_original, (reduzida_w, reduzida_h))
        self.estrela_esquerda = pygame.transform.flip(self.estrela_direita, True, False)

        self.estrela_frame_width = reduzida_w
        self.estrela_frame_height = reduzida_h

        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.mp3")

        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50
        self.z_pressed_last_frame = False

    def update(self, keys, joystick=None):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        dx = 0

        jump_pressed = keys[pygame.K_SPACE]
        fire_pressed = keys[pygame.K_z]
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]

        if joystick:
            axis_0 = joystick.get_axis(0)
            joystick_dx = axis_0

            if axis_0 < -0.3:
                move_left = True
            elif axis_0 > 0.3:
                move_right = True

            jump_pressed = jump_pressed or joystick.get_button(0)

            fire_pressed = fire_pressed or joystick.get_button(2)


            jump_pressed = jump_pressed or joystick.get_button(0)
            fire_pressed = fire_pressed or joystick.get_button(2)

        if fire_pressed and not self.z_pressed_last_frame:
            direction = self.last_direction
            estrela_sprite = self.estrela_direita if direction == 1 else self.estrela_esquerda

            estrela = PoderBase(
                self.rect.centerx,
                self.rect.centery,
                direction,
                estrela_sprite,
                frame_count=1,
                frame_width=self.estrela_frame_width,
                frame_height=self.estrela_frame_height
            )
            self.poder_group.add(estrela)

        self.z_pressed_last_frame = fire_pressed

        if move_left:
            dx = -self.speed
            self.last_direction = -1
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_left = (self.frame_left + 1) % len(self.mabel_anim_left)
                self.image = self.mabel_anim_left[self.frame_left]

        elif move_right:
            dx = self.speed
            self.last_direction = 1
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_right = (self.frame_right + 1) % len(self.mabel_anim_right)
                self.image = self.mabel_anim_right[self.frame_right]

        else:
            self.image = self.image_idle

        if jump_pressed and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()

        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        self.poder_group.update()



    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.poder_group.draw(screen)
