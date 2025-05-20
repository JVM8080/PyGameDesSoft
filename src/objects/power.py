import pygame

class PoderBase(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, spritesheet, frame_count, frame_width, frame_height, speed=9):
        super().__init__()
        self.frames = []
        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()

        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 80  # milissegundos entre quadros

        self.direction = direction
        self.speed = speed

    def update(self):
        # Movimento
        self.rect.x += self.speed * self.direction

        # Animação
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Remove se sair da tela
        if self.rect.right < 0 or self.rect.left > 800:  # largura da tela
            self.kill()   
    