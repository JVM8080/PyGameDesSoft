import pygame
from src.objects.player_mable import Player
from config import HEIGHT, FPS
from src.utils.asset_loader import load_image

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    # Carrega e redimensiona o fundo para o tamanho da tela
    background = load_image("mabel/imagem level 1.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()
        player.update(keys)

        screen.blit(background, (0, 0))  # desenha o fundo
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
