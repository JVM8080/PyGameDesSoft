import pygame
from config import HEIGHT, WIDTH, FPS
from src.objects.player_mable import Player
from src.utils.asset_loader import load_image
from src.objects.platforma_level1 import Platform
from src.screens.pause_screen import PauseScreen


def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 350)
    player.on_ground = False

    background = load_image("mabel/imagem level 1.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Plataformas
    platforms = pygame.sprite.Group()
    platform_surface = load_image("mabel/plataforma3_limpa.png")
    small_w, small_h = 50, 30
    large_w, large_h = 180, 60

    platform2 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), screen_width - large_w - 60, HEIGHT - 180)
    platform3 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), screen_width // 2 - large_w // 2, HEIGHT - 260)
    platform4 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), 60, HEIGHT - 180)

    platforms.add(platform2, platform3, platform4)

    # Verificación inicial de colisión
    for plat in platforms:
        if player.rect.colliderect(plat.rect):
            player.rect.bottom = plat.rect.top
            player.vel_y = 0
            player.on_ground = True
            break

    # Pantalla de pausa
    pause_screen = PauseScreen(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if pause_screen.active:
                action = pause_screen.handle_event(event)
                if action == 'continue':
                    pause_screen.hide()
                elif action == 'menu':
                    return 'menu'
                elif action == 'level_select':
                    return 'level_select'
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_screen.show()

        if pause_screen.active:
            pause_screen.update(dt)
            screen.blit(background, (0, 0))
            platforms.update()
            for p in platforms:
                p.draw(screen)
            player.draw(screen)
            pause_screen.draw()
            pygame.display.flip()
            continue

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

        if player.rect.bottom == screen_height and not any(player.rect.colliderect(p.rect) for p in platforms):
            player.on_ground = True

        # Colisiones
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

        if not collided and player.rect.bottom < screen_height:
            player.on_ground = False



        # Render
        screen.blit(background, (0, 0))
        platforms.update()
        for p in platforms:
            p.draw(screen)
        player.draw(screen)
        pygame.display.flip()
