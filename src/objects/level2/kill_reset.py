import pygame

class Portal(pygame.sprite.Sprite):
    frame_index_global = 0
    last_update_global = pygame.time.get_ticks()

    def __init__(self, x, y, spritesheet, frame_width=24, frame_height=32, frame_count=8, frame_speed=100):
        super().__init__()
        self.frames = []
        self.frame_speed = frame_speed

        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames.append(frame)

        self.image = self.frames[Portal.frame_index_global]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - Portal.last_update_global > self.frame_speed:
            Portal.last_update_global = now
            Portal.frame_index_global = (Portal.frame_index_global + 1) % len(self.frames)
        self.image = self.frames[Portal.frame_index_global]
