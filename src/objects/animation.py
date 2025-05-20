
import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, frame_width=24, frame_height=32, frame_count=8, frame_speed=100, scale_size=None):
        super().__init__()
        self.frames = []
        self.frame_speed = frame_speed
        self.scale_size = scale_size if scale_size else (200, 200)
        self.fixed_x = x
        self.fixed_y = y

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            self.frames.append(frame)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.fixed_x, self.fixed_y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.image = self.frames[self.frame_index]
        self.rect.topleft = (self.fixed_x, self.fixed_y)


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, flight_sheet, attack_sheet, target, scale_size=(300, 300), speed=1):
        super().__init__()

        self.hit_frames = self.load_frames(pygame.image.load("assets/images/level2/Take Hit.png").convert_alpha(), 4, scale_size)
        self.death_frames = self.load_frames(pygame.image.load("assets/images/level2/Death.png").convert_alpha(), 6, scale_size)
        self.dead = False
        self.hit = False
        self.death_timer = 0
        self.flight_frames = self.load_frames(flight_sheet, 8, scale_size)
        self.attack_frames = self.load_frames(attack_sheet, 8, scale_size)
        self.image = self.flight_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vida = 2

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 100

        self.state = "fly"
        self.target = target
        self.speed = speed

    def load_frames(self, sheet, count, scale_size):
        frames = []
        width = sheet.get_width() // count
        height = sheet.get_height()
        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
            frame = pygame.transform.scale(frame, scale_size)
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()

        if self.dead:
            # Animação de morte
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.frame_index]
            return

        if self.hit:
            # Animação de dano
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.hit_frames):
                    self.hit = False
                    self.state = "fly"
                    self.frame_index = 0
                else:
                    self.image = self.hit_frames[self.frame_index]
            return

        # Movimento em direção ao player
        enemy_center = self.rect.center
        target_center = self.target.rect.center
        dx = dy = 0
        if enemy_center[0] < target_center[0]:
            dx = self.speed
        elif enemy_center[0] > target_center[0]:
            dx = -self.speed

        if enemy_center[1] < target_center[1]:
            dy = self.speed
        elif enemy_center[1] > target_center[1]:
            dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Checar proximidade para trocar estado
        distance_x = abs(self.rect.centerx - self.target.rect.centerx)
        distance_y = abs(self.rect.centery - self.target.rect.centery)
        if distance_x < 20 and distance_y < 20:
            self.state = "attack"
        else:
            self.state = "fly"

        # Animação normal (voando ou atacando)
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % 8
            if self.state == "fly":
                self.image = self.flight_frames[self.frame_index]
            elif self.state == "attack":
                self.image = self.attack_frames[self.frame_index]

        # Verificar colisão com poderes
        for poder in self.target.poder_group:
            if now - poder.spawn_time < 50:
                continue
            if self.rect.colliderect(poder.rect):
                self.vida -= 1
                self.hit = True
                self.state = "hit"
                self.frame_index = 0
                self.last_update = now
                poder.kill()

        # Verificar morte
        if self.vida <= 0 and not self.dead:
            self.dead = True
            self.state = "dead"
            self.frame_index = 0
            self.last_update = now


        

