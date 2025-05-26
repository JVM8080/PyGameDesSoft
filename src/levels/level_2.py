import pygame
import os
from src.objects.player_stan import Player
from src.objects.platforms import Platform
from config import *
from src.utils.asset_loader import load_image
from src.objects.animation import *
from src.objects.decoration import *
import random
from src.screens.game_over import tela_game_over


def run(screen):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/level2_audio/level2.ogg")
    pygame.mixer.music.set_volume(1)  # volume de 0.0 a 1.0
    pygame.mixer.music.play(-1)  # -1 faz repetir infinitamente
    som_morte = pygame.mixer.Sound("assets/sounds/level2_audio/stan_death.wav")
    som_morte.set_volume(0.5)  # volume de 0.0 a 1.0

    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    pygame.font.init()
    fonte_sacos = pygame.font.SysFont('arial', 40, bold=True)
    icone_dinheiro = pygame.image.load("assets/images/level2/money_bag.png").convert_alpha()
    icone_dinheiro = pygame.transform.scale(icone_dinheiro, (90, 90))  

    jogador_morreu = False
    momento_morte = 0

    diagramas_pendentes = []
    diagrama_animado_group = pygame.sprite.Group()
    diagrama_disparado = False
    bill_image = pygame.image.load("assets/images/level2/angrybill.png").convert_alpha()
    bill_group = pygame.sprite.Group()


    player_group = pygame.sprite.Group(player)
    totem = carregar_imagem_totem()
    fire = carregar_imagem_fogo()
    fire_group = pygame.sprite.Group(fire)

    platforms = pygame.sprite.Group(
        Platform("assets/images/level2/base.png", 0, HEIGHT-60, 800, 100),
        Platform("assets/images/level2/plataforma central.png", 215, HEIGHT/2+50, 375, 50),
        Platform("assets/images/level2/plataformas laterais.png", -40, HEIGHT-150, 200, 50),
        Platform("assets/images/level2/plataformas laterais.png", WIDTH-160, HEIGHT-150, 200, 50),
        Platform("assets/images/level2/plataforma superior.png", 0, HEIGHT/2-70, 130, 100),
        Platform("assets/images/level2/plataforma superior.png", WIDTH-130, HEIGHT/2-70, 130, 100)
    )

    money_sheet = pygame.image.load("assets/images/level2/money.png").convert_alpha()
    money_group = pygame.sprite.Group(MoneyBag(money_sheet, platforms, player))

    flight_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Flight.png")).convert_alpha()
    attack_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Attack1.png")).convert_alpha()
    zombie_walk_sheet = pygame.image.load("assets/images/level2/Zombie correndo.png").convert_alpha()
    zombie_attack_sheet = pygame.image.load("assets/images/level2/Zombie atacando.png").convert_alpha()
    portal_sheet = pygame.image.load("assets/images/level2/portal opening.png").convert_alpha()

    enemies = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()

    zombie_spawns = pygame.sprite.Group(
        ZombieSpawn(300, HEIGHT/2 - 20, enemies, player, fire, platforms, zombie_walk_sheet, zombie_attack_sheet)
    )

    for x, y in [(250, HEIGHT/2 - 20), (350, HEIGHT/2 - 20), (400, HEIGHT/2 - 20)]:
        zombie_spawns.add(ZombieSpawn(x, y, enemies, player, fire, platforms, zombie_walk_sheet, zombie_attack_sheet))

    spawn_points = [(70, 200), (WIDTH - 60, 150), (70, 150), (WIDTH - 60, 200)]
    for ponto in random.sample(spawn_points, random.randint(1, min(3, len(spawn_points)))):
        portal_group.add(PortalSpawn(*ponto, portal_sheet, enemies, player, flight_sheet, attack_sheet))

    spawn_timer = pygame.time.get_ticks()
    spawn_interval = 10000

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not jogador_morreu and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return 'menu'

        keys = pygame.key.get_pressed()

        background = pygame.image.load("assets/images/level2/cenario level 2.jpeg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        graves1 = load_image('level2/tumulos.png', size=(370, 70))
        graves2 = load_image('level2/graves.png', size=(370, 70))

        screen.blit(background, (0, -10))
        platforms.draw(screen)
        fire_group.update()
        fire_group.draw(screen)
        screen.blit(graves1, (235, HEIGHT/2 - 15))
        screen.blit(graves2, (220, HEIGHT/2 - 10))
        totem.update()
        screen.blit(totem.image, (10, 130))
        screen.blit(totem.image, (WIDTH - 120, 130))

        if jogador_morreu:
            pygame.mixer.music.stop()
            som_morte.play()
            tempo_morrido = pygame.time.get_ticks() - momento_morte
            desenhar_vidas(screen, player.vida)
            player_group.draw(screen)
            money_group.draw(screen)
            pygame.display.flip()
            if tempo_morrido > 3000:
                return tela_game_over(screen)
            clock.tick(60)
            continue


        player_group.update(keys, platforms)
        if not jogador_morreu and player.vida <= 0:
            jogador_morreu = True
            momento_morte = pygame.time.get_ticks()
            print("💀 O jogador morreu, vida zerada")

        if not jogador_morreu and player.rect.colliderect(fire.hitbox):
            jogador_morreu = True
            momento_morte = pygame.time.get_ticks()
            print("🔥 O jogador morreu no fogo")

        player_group.draw(screen)
        money_group.draw(screen)
        desenhar_vidas(screen, player.vida)
        desenhar_contador_sacos(screen, fonte_sacos, player.dinheiro)
        screen.blit(icone_dinheiro, (WIDTH - 230, 15))  # posição ajustável
        desenhar_contador_sacos(screen, fonte_sacos, player.dinheiro)

        for money in money_group:
            resultado = money.update()
            if resultado == 'win':
                pygame.mixer.music.stop()
                pygame.display.flip()  # Atualiza a tela uma última vez
                pygame.time.delay(3000)  # Espera 3 segundos travado
                return tela_vitoria(screen)
            
        enemies.update()
        for enemy in enemies:
            if isinstance(enemy, ZombieEnemy) and fire.hitbox.colliderect(enemy.rect) and not enemy.ativou_diagrama:
                enemy.ativou_diagrama = True
                enemy.dead = True
                enemy.state = "dead"
                enemy.frame_index = 0
                enemy.last_update = pygame.time.get_ticks()
                enemy.frame_speed = 150  # ou outro valor adequado
                diagrama = DiagramaAnimado("assets/images/level2/diagrama", pos=(WIDTH // 2, 180), frame_speed=50, scale=0.3)
                diagrama_animado_group.add(diagrama)
                diagramas_pendentes.append(diagrama)
                print("⚠️ Zumbi ativou o diagrama e morreu no fogo!")

        enemies.draw(screen)
        zombie_spawns.update()
        zombie_spawns.draw(screen)

        portal_group.update()
        for portal in portal_group:
            scaled = pygame.transform.scale(portal.image, (40, 40))
            screen.blit(scaled, scaled.get_rect(center=portal.rect.center).topleft)

        player.poder_group.draw(screen)

        now = pygame.time.get_ticks()
        if now - spawn_timer > spawn_interval:
            spawn_timer = now
            for ponto in random.sample(spawn_points, random.randint(1, 3)):
                portal_group.add(PortalSpawn(*ponto, portal_sheet, enemies, player, flight_sheet, attack_sheet))
            spawn_interval = random.randint(10000, 15000)

        diagrama_animado_group.update()
        for diagrama in diagramas_pendentes[:]:  # cópia da lista para iterar com segurança
            if diagrama.terminou:
                bill_group.add(BillCipherChaser(WIDTH // 2, HEIGHT // 2, bill_image, player))
                diagramas_pendentes.remove(diagrama)

        diagrama_animado_group.draw(screen)
        bill_group.update()
        bill_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
