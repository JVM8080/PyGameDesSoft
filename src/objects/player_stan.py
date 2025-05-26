import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer
from src.objects.power import PoderBase

JUMP_SOUND = None

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # chama o init da classe Sprite

        global JUMP_SOUND

        self.image_idle = load_image("level2/stan/stan parado.png").convert_alpha()
        self.anim_left = load_image('level2/stan/stan indo pra esquerda.png').convert_alpha()
        self.anim_right = load_image('level2/stan/stan indo pra direita.png').convert_alpha()

        frame_width = self.anim_left.get_width()//3
        frame_height = self.anim_left.get_height()

        self.stan_anim_left = []
        for i in range(3):
            frame = self.anim_left.subsurface(i * frame_width, 0, frame_width, frame_height)
            self.stan_anim_left.append(frame)

        self.stan_anim_right = []
        for i in range(3):
            frame = self.anim_right.subsurface(i * frame_width, 0, frame_width, frame_height)
            self.stan_anim_right.append(frame)

        self.frame_left = 0
        self.frame_right = 0

        self.image = self.stan_anim_right[self.frame_right]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.speed = 5
        self.jump_force = -8
        self.gravity = 0.3
        self.on_ground = False
        self.last_shoot_direction = -1  # -1 = esquerda, 1 = direita

        self.vida = 10
        self.dinheiro = 0 
        self.enemy_group = pygame.sprite.Group()

        self.morto_no_fogo = False
        self.momento_morte = 0

        self.poder_group = pygame.sprite.Group()
        self.moeda_spritesheet = load_image("level2/stan/poder moedas.png").convert_alpha()

        # Valores fixos da sua imagem
        self.moeda_frame_width = self.moeda_spritesheet.get_width() // 6
        self.moeda_frame_height = self.moeda_spritesheet.get_height()

        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.mp3")

        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50

        self.z_pressed_last_frame = False

    def update(self, keys, platforms, joystick=None):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        dx = 0
        dy = 0

        # === INPUTS DE MOVIMIENTO ===
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]

        if joystick:
            axis_x = joystick.get_axis(0)
            move_left = move_left or axis_x < -0.2
            move_right = move_right or axis_x > 0.2

        if move_left:
            dx = -self.speed
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_left = (self.frame_left + 1) % len(self.stan_anim_left)
                self.image = self.stan_anim_left[self.frame_left]
                self.last_shoot_direction = -1

        elif move_right:
            dx = self.speed
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_right = (self.frame_right + 1) % len(self.stan_anim_right)
                self.image = self.stan_anim_right[self.frame_right]
                self.last_shoot_direction = 1
        else:
            self.image = self.image_idle

        # === SALTO (tecla SPACE o botón A) ===
        jump_pressed = keys[pygame.K_SPACE]
        if joystick:
            jump_pressed = jump_pressed or joystick.get_button(0)  # Botón A

        if jump_pressed and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()

        # === DISPARO (tecla Z o botón X) ===
        shoot_pressed = keys[pygame.K_z]
        if joystick:
            shoot_pressed = shoot_pressed or joystick.get_button(2)  # Botón X

        if shoot_pressed and not self.z_pressed_last_frame:
            direction = self.last_shoot_direction
            offset = 30
            moeda = PoderBase(
                self.rect.centerx + direction * offset,
                self.rect.centery,
                direction,
                self.moeda_spritesheet,
                frame_count=6,
                frame_width=self.moeda_frame_width,
                frame_height=self.moeda_frame_height
            )
            self.poder_group.add(moeda)

        self.z_pressed_last_frame = shoot_pressed

        # === FÍSICA ===
        self.vel_y += self.gravity
        dy = self.vel_y
        self.rect.x += dx
        self.rect.y += dy

        # COLISÕES COM PLATAFORMAS
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        if jump_button and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()

        self.jump_pressed_last_frame = jump_button

        self.poder_group.update()

        # COLISÕES COM INIMIGOS
        for enemy in pygame.sprite.spritecollide(self, self.enemy_group, False):
            if enemy.state == "attack":
                if not hasattr(enemy, "last_hit") or pygame.time.get_ticks() - enemy.last_hit > 500:
                    self.vida -= 1
                    enemy.last_hit = pygame.time.get_ticks()
                    print(f"Player levou dano! Vida: {self.vida}")
                if self.vida <= 0:
                    self.kill()



    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.poder_group.draw(screen)


        