import pygame
from src.objects.player_mable import Player
from config import HEIGHT, FPS
from src.utils.asset_loader import load_image
from src.objects.platforma_level1 import Platform
from src.objects.gnomo_inimigo import GnomoInimigo
from src.objects.porquinho import Porquinho

def run(screen):
    clock = pygame.time.Clock()
    pygame.font.init()
    font_porcos = pygame.font.SysFont("arial", 24)

    player = Player(100, HEIGHT - 350)
    player.on_ground = False

    background = load_image("mabel/imagem level 1.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Arco-íris visível
    rainbow_image = load_image("rainbow_large_from_original.png")
    rainbow_image = pygame.transform.scale(rainbow_image, (300, 200))
    rainbow_rect = rainbow_image.get_rect(midtop=(screen_width // 2, 0))
    arco_rect = rainbow_rect

    # Plataformas
    platforms = pygame.sprite.Group()
    platform3_surface = load_image("mabel/plataforma3_limpa.png")
    large_width, large_height = 180, 60

    platform2 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), screen_width - large_width - 60, HEIGHT - 180)
    platform3 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), screen_width // 2 - large_width // 2, HEIGHT - 260)
    platform4 = Platform(pygame.transform.scale(platform3_surface, (large_width, large_height)), 60, HEIGHT - 180)
    platforms.add(platform2, platform3, platform4)

    for plat in platforms:
        if player.rect.colliderect(plat.rect):
            player.rect.bottom = plat.rect.top
            player.vel_y = 0
            player.on_ground = True
            break

    # Gnomos
    gnomo_group = pygame.sprite.Group()
    last_gnomo_spawn = pygame.time.get_ticks()
    intervalo_gnomo = 2000

    # Porquinhos
    porcos_group = pygame.sprite.Group()
    coletados = 0
    last_spawn_time = pygame.time.get_ticks()
    intervalo_spawn = 4000

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()
        player.update(keys)

        now = pygame.time.get_ticks()

        # Porquinho a cada 4s sobre plataforma ou chão
        if now - last_spawn_time > intervalo_spawn:
            import random
            spawnou = False
            plataformas_lista = list(platforms)
            random.shuffle(plataformas_lista)
            for plat in plataformas_lista:
                porco = Porquinho()
                porco.rect.midbottom = (random.randint(plat.rect.left + 10, plat.rect.right - 10), plat.rect.top)
                porcos_group.add(porco)
                spawnou = True
                break
            if not spawnou:
                porco = Porquinho()
                porco.rect.midbottom = (random.randint(50, screen_width - 50), HEIGHT)
                porcos_group.add(porco)
            last_spawn_time = now

        # Gnomo do arco-íris
        if now - last_gnomo_spawn > intervalo_gnomo:
            novo_gnomo = GnomoInimigo(arco_rect, player, platforms)
            gnomo_group.add(novo_gnomo)
            last_gnomo_spawn = now

        # Coleta porcos
        colididos = pygame.sprite.spritecollide(player, porcos_group, True)
        coletados += len(colididos)
        if coletados >= 20:
            return 'level_2'

        # Limites da Mabel
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

        # Atualizações
        gnomo_group.update()
        porcos_group.update()

        # Desenho
        screen.blit(background, (0, 0))
        screen.blit(rainbow_image, rainbow_rect)
        for p in platforms:
            p.draw(screen)

        player.draw(screen)
        gnomo_group.draw(screen)
        porcos_group.draw(screen)

        texto_porcos = font_porcos.render(f"Porcos: {coletados}/20", True, (255, 255, 255))
        screen.blit(texto_porcos, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)
