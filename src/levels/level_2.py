import pygame
from src.objects.player_stan import Player
from src.objects.platforms import Platform
from config import *

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
        background = pygame.image.load("assets/images/level2/cenario level 2.jpeg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        platforms = pygame.sprite.Group()
        p1 = Platform("assets/images/level2/base.png", 0, HEIGHT-60, width=800, height=100)
        platforms.add(p1)

        screen.blit(background, (0, 0)) 
        platforms.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
