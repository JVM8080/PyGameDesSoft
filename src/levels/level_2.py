import pygame
from src.objects.player_stan import Player
from config import HEIGHT, FPS

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.fill((100, 200, 100)) 
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
