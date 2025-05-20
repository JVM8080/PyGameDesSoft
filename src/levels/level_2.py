import pygame
import os
from src.objects.player_stan import Player
from src.objects.platforms import Platform
from config import *
from src.utils.asset_loader import load_image
from src.objects.animation import Portal, FlyingEnemy
from src.objects.decoration import *

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    player_group = pygame.sprite.Group()
    player_group.add(player)


    # carrega o totem uma única vez
    totem = carregar_imagem_totem()
    fire = carregar_imagem_fogo()
    fire_group = pygame.sprite.Group(fire)

    # Carregar sprites dos inimigos
    flight_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Flight.png")).convert_alpha()
    attack_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Attack1.png")).convert_alpha()

    # Criar inimigo voador
    enemies = pygame.sprite.Group()
    enemy = FlyingEnemy(500, 100, flight_sheet, attack_sheet, player)
    enemies.add(enemy)
    player.enemy_group.add(enemy)  


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()

        screen.fill((100, 200, 100)) 
        background = pygame.image.load("assets/images/level2/cenario level 2.jpeg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        platforms = pygame.sprite.Group()
        p1 = Platform("assets/images/level2/base.png", 0, HEIGHT-60, width=800, height=100)
        p2 = Platform("assets/images/level2/plataforma central.png", 215, HEIGHT/2+50, width=375, height=50)
        p3 = Platform("assets/images/level2/plataformas laterais.png", -40, HEIGHT-150, width=200, height=50)
        p4 = Platform("assets/images/level2/plataformas laterais.png", WIDTH-160, HEIGHT-150, width=200, height=50) 
        p5 = Platform("assets/images/level2/plataforma superior.png", 0, HEIGHT/2-70, width=130, height=100) 
        p6 = Platform("assets/images/level2/plataforma superior.png", WIDTH-130, HEIGHT/2-70, width=130, height=100) 
        platforms.add(p1, p2, p3, p4, p5, p6)

        graves1 = load_image('level2/tumulos.png', size=(370, 70))
        graves2 = load_image('level2/graves.png', size=(370, 70))
        clouds = load_image('level2/nuvens.png', (900, 150))

        player_group.update(keys, platforms)
        enemies.update()

        screen.blit(background, (0, -10)) 
        platforms.draw(screen)
        fire_group.update()
        fire_group.draw(screen)

        screen.blit(graves1, (235, HEIGHT/2-15))
        screen.blit(graves2, (220, HEIGHT/2-10))
        screen.blit(clouds, (-30, -30))

        totem.update()
        screen.blit(totem.image, (10, 130))
        screen.blit(totem.image, (WIDTH-120, 130))

        player_group.draw(screen)
        enemies.draw(screen)

        # redesenhar a moeda por cima
        player.poder_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)
