import pygame
import random
from src.objects.dipper import Player
from src.objects.enemigo import Enemy
from src.objects.bill import Bill
from src.objects.platform import Platform

from src.utils.asset_loader import load_image
from config import HEIGHT, WIDTH, FPS

from src.screens.game_over_screen import GameOverScreen
from src.screens.pause_screen import PauseScreen
from src.screens.level_complete_screen import LevelCompleteScreen

def run(screen):
    clock = pygame.time.Clock()
    dt = clock.tick(FPS)
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    enemy_spawn_delay = 1000  

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
    level_complete = False  

    game_over_screen = GameOverScreen(screen)
    pause_screen = PauseScreen(screen)
    level_complete_screen = LevelCompleteScreen(screen)
    
    platforms = pygame.sprite.Group()
    
    platforms.add(Platform(150, 400, phase=0))
    platforms.add(Platform(350, 450, phase=45))
    platforms.add(Platform(550, 400, phase=90))
    starting_platform = list(platforms)[1]  
    
    player_x = starting_platform.rect.x + starting_platform.rect.width // 2
    player_y = starting_platform.rect.y - 60  

    player = Player(player_x, player_y)
    
    bills = pygame.sprite.Group()
    bill = Bill(WIDTH // 2, 150, phase=0)
    bills.add(bill)

    while running:
        dt = clock.tick(FPS)
        enemy_spawn_timer += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if game_over:
                result = game_over_screen.handle_event(event)
                if result == 'reset':
                    player = Player(player_x, player_y)                    
                    enemies.empty()
                    bills.empty()  
                    bill = Bill(WIDTH // 2, 150, phase=0)
                    bills.add(bill)
                    lives = 3
                    enemy_spawn_timer = 0
                    game_over = False
                elif result == 'menu':
                    return 'menu'
                    
            elif level_complete:
                result = level_complete_screen.handle_event(event)
                if result == 'restart':
                    player = Player(player_x, player_y)
                    enemies.empty()
                    bills.empty()
                    bill = Bill(WIDTH // 2, 150, phase=0)
                    bills.add(bill)
                    lives = 3
                    enemy_spawn_timer = 0
                    level_complete = False
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

        if not game_over and not paused and not level_complete:
            player.update(keys=keys, joystick=joystick, platforms=platforms)

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

            projectiles_to_remove = []

            for projectile in player.projectiles.copy():
                removed = False

                for enemy in enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        enemy.health -= getattr(projectile, 'damage', 1)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        projectiles_to_remove.append(projectile)
                        removed = True
                        break  
                if not removed and bill.rect.colliderect(projectile.rect):
                    bill.health -= projectile.damage
                    if bill.health <= 0:
                        bill.kill()
                        level_complete = True
                        enemies.empty()
                        player.projectiles.clear()
                        player.special_attacks.clear()
                    projectiles_to_remove.append(projectile)

            for projectile in projectiles_to_remove:
                if projectile in player.projectiles:
                    player.projectiles.remove(projectile)

            for bill in bills.copy():
                if player.rect.colliderect(bill.rect):
                    if not player.invulnerable:
                        lives -= 1
                        player.activate_invulnerability()
                        player.play_damage_animation()
                        if lives <= 0:
                            game_over = True
                            enemies.empty()
                            player.projectiles.clear()
                            player.special_attacks.clear()
                            
            for attack in player.special_attacks.copy():
                hit = False
                for enemy in enemies.copy():
                    if attack.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        hit = True
                        break

                if bill.rect.colliderect(attack.rect):
                    bill.health -= getattr(attack, 'damage', 6)
                    if bill.health <= 0:
                        bill.kill()
                        level_complete = True
                    hit = True

                if hit:
                    player.special_attacks.remove(attack)

            if enemy_spawn_timer >= enemy_spawn_delay and not level_complete:
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

        background_path = "level_3/background_2.png" if bill.is_damaged else "level_3/background_1.png"
        screen.blit(load_image(background_path, size=("auto", HEIGHT)), (0, 0))

        player.draw(screen)
        enemies.draw(screen)
        platforms.update()
        platforms.draw(screen)
        if not level_complete:
            bill.update(dt, player.rect)
            bills.draw(screen)

            if bill.alive():
                bar_width = 200
                bar_height = 20
                bar_x = (WIDTH - bar_width) // 2
                bar_y = 20

                health_ratio = max(bill.health, 0) / bill.max_health
                current_bar_width = int(bar_width * health_ratio)

                pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height)) 
                pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_bar_width, bar_height))  

        if paused:
            pause_screen.draw()

        if game_over:
            game_over_screen.draw()
            
        if level_complete:
            level_complete_screen.draw()

        pygame.display.flip()