import pygame
import random
from src.objects.dipper import Player
from src.objects.enemigo import Enemy
from src.utils.asset_loader import load_image
from config import HEIGHT, WIDTH, FPS

from src.screens.game_over_screen import GameOverScreen
from src.screens.pause_screen import PauseScreen

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    enemy_spawn_delay = 500  

    lives = 3
    font = pygame.font.SysFont(None, 36)

    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    running = True
    game_over = False
    paused = False

    game_over_screen = GameOverScreen(screen)
    pause_screen = PauseScreen(screen)

    while running:
        dt = clock.tick(FPS)
        enemy_spawn_timer += dt
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if game_over:
                result = game_over_screen.handle_event(event)
                if result == 'reset':
                    player = Player(100, HEIGHT - 150)
                    enemies.empty()
                    lives = 3
                    enemy_spawn_timer = 0
                    game_over = False
                elif result == 'menu':
                    return 'menu'

            elif paused:
                result = pause_screen.handle_event(event)
                if result == 'continue':
                    paused = False
                elif result == 'level_select':
                    return 'level_select'
                elif result == 'menu':
                    return 'menu'

            else:  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:  
                        paused = not paused

        keys = pygame.key.get_pressed()

        if not game_over and not paused:
            player.update(keys=keys, joystick=joystick)

            for enemy in enemies.copy():
                enemy.update(player.rect)
                if player.rect.colliderect(enemy.rect):
                    if not player.invulnerable:
                        lives -= 1
                        player.activate_invulnerability()
                        player.play_damage_animation()  
                        enemies.remove(enemy)
                        if lives <= 0:
                            game_over = True
                            enemies.empty()
                            player.projectiles.clear()
                            player.special_attacks.clear()

            for projectile in player.projectiles.copy():
                for enemy in enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        enemy.health -= getattr(projectile, 'damage', 1)  # Si el projectile no tiene damage, asume 1
                        player.projectiles.remove(projectile)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        break


            for attack in player.special_attacks.copy():
                for enemy in enemies.copy():
                    if attack.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        player.special_attacks.remove(attack)
                        break

            if enemy_spawn_timer >= enemy_spawn_delay:
                spawn_side = random.choice(['top', 'left', 'right'])
                if spawn_side == 'top':
                    enemy_x = random.randint(0, WIDTH - 40)
                    enemy_y = -40
                elif spawn_side == 'left':
                    enemy_x = -40
                    enemy_y = random.randint(0, HEIGHT - 40)
                else:  
                    enemy_x = WIDTH + 40
                    enemy_y = random.randint(0, HEIGHT - 40)

                enemy = Enemy(enemy_x, enemy_y)
                enemies.add(enemy)
                enemy_spawn_timer = 0

        screen.blit(load_image("level_3/background_1.png", size=("auto", HEIGHT)), (0, 0))
        player.draw(screen)
        enemies.draw(screen)
        lives_text = font.render(f"Vidas: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        if paused:
            pause_screen.draw()

        if game_over:
            game_over_screen.draw()

        pygame.display.flip()
