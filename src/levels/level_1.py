import pygame
from src.objects.player_mable import Player
from config import HEIGHT, FPS
from src.utils.asset_loader import load_image
from src.objects.platforma_level1 import Platform

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 350)
    player.on_ground = False  # assume que começa no ar

    # Fundo
    background = load_image("mabel/imagem level 1.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Plataformas
    platforms = pygame.sprite.Group()
    platform1_surface = load_image("mabel/plataforma1_limpa.png")
    platform2_surface = load_image("mabel/plataforma2_limpa.png")
    platform3_surface = load_image("mabel/plataforma3_limpa.png")
    

    # Ajuste de tamanho
    small_width, small_height = 50, 30
    large_width, large_height = 180, 60

    platform2 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), screen_width - large_width - 60, HEIGHT - 180)
    platform3 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), screen_width // 2 - large_width // 2, HEIGHT - 260)
    

    platform4 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), 60, HEIGHT - 180)
    platforms.add( platform2, platform3, platform4)

    # Verifica colisão inicial com chão/plataforma
    for plat in platforms:
        if player.rect.colliderect(plat.rect):
            player.rect.bottom = plat.rect.top
            player.vel_y = 0
            player.on_ground = True
            break

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Limites da tela
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width:
            player.rect.right = screen_width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > screen_height:
            player.rect.bottom = screen_height
            player.vel_y = 0
            player.on_ground = True

        # Reforça detecção de chão logo ao início
        if player.rect.bottom == screen_height and not any(player.rect.colliderect(p.rect) for p in platforms):
            player.on_ground = True

        # Colisão com plataformas - lógica mais permissiva
        collided = False
        for plat in platforms:
            if player.vel_y > 0:
                tolerance = 10
                if (
                    player.rect.bottom <= plat.rect.top + tolerance and
                    player.rect.bottom + player.vel_y >= plat.rect.top and
                    player.rect.right > plat.rect.left + 5 and
                    player.rect.left < plat.rect.right - 5
                ):
                    player.rect.bottom = plat.rect.top
                    player.vel_y = 0
                    player.on_ground = True
                    collided = True
                    break

        if not collided:
            # Só considera que está no ar se não está encostando no chão
            if player.rect.bottom < screen_height:
                player.on_ground = False

        # Desenho
        screen.blit(background, (0, 0))
        platforms.update()
        for p in platforms:
            p.draw(screen)

        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
