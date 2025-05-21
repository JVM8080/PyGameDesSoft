import pygame
from config import *

def tela_game_over(screen):
    gameover_img = pygame.image.load("assets/images/GameOver.png").convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'

        screen.blit(gameover_img, (0, 0))
        pygame.display.flip()
        clock.tick(60)
