import pygame
from config import HEIGHT
from src.utils.safe_asset_loader import load_image_safe as load_image

class GnomoInimigo(pygame.sprite.Sprite):
    def __init__(self, arco_rect, player, plataformas):
        super().__init__()
        self.player = player
        self.plataformas = plataformas

        self.speed = 1.6
        self.gravity = 0.4
        self.vel_y = 0
        self.jump_force = -14
        self.dano = 1
        self.cooldown = 1000
        self.last_hit = 0
        self.hp = 1
        self.on_ground = False

        self.frames = {
            "down": self.split_sheet(load_image("gnome_down_up.png")),
            "left": self.split_sheet(load_image("gnome_left.png")),
            "right": self.split_sheet(load_image("gnome_right.png")),
            "up": self.split_sheet(load_image("gnome_down_up.png")),
        }

        self.direction = "down"
        self.frame_index = 0
        self.image = self.frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect(midbottom=(arco_rect.centerx, arco_rect.bottom))

        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 150

        self.reaction_timer = pygame.time.get_ticks()
        self.reaction_delay = 400  # para não pular sempre

    def split_sheet(self, sheet):
        frame_width = sheet.get_width() // 3
        frame_height = sheet.get_height()
        return [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(3)]

    def update(self):
        now = pygame.time.get_ticks()
        dx = 0
        dy = self.vel_y

        px, py = self.player.rect.center
        gx, gy = self.rect.center
        dist_x = px - gx
        dist_y = py - gy

        horizontal_prox = abs(dist_x) < 300

        # Sempre tenta se mover no eixo X em direção à Mabel
        if horizontal_prox:
            dx = self.speed if dist_x > 0 else -self.speed
            self.direction = "right" if dx > 0 else "left"

        # Se Mabel estiver acima e próxima, tenta pular
        if (
            py < self.rect.centery - 60 and
            abs(dist_x) < 100 and
            self.on_ground and
            now - self.reaction_timer > self.reaction_delay
        ):
            self.vel_y = self.jump_force
            self.reaction_timer = now

        # Gravidade
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Colisão com plataformas
        self.on_ground = False
        for plat in self.plataformas:
            if self.vel_y >= 0:
                if (
                    self.rect.bottom <= plat.rect.top + 10 and
                    self.rect.bottom + self.vel_y >= plat.rect.top and
                    self.rect.right > plat.rect.left + 5 and
                    self.rect.left < plat.rect.right - 5
                ):
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    break

        # Chão
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Animação
        if now - self.frame_timer >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
            self.frame_timer = now

        self.image = self.frames[self.direction][self.frame_index]

        # Dano à Mabel
        if self.rect.colliderect(self.player.rect):
            if now - self.last_hit > self.cooldown:
                if hasattr(self.player, 'vida'):
                    self.player.vida -= self.dano
                self.last_hit = now

        # Leva hit e morre
        for poder in self.player.poder_group:
            if self.rect.colliderect(poder.rect):
                self.hp -= 1
                poder.kill()
                if self.hp <= 0:
                    self.kill()
