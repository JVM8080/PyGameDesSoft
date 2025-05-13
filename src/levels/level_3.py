import pygame
from src.objects.dipper import Player
from config import HEIGHT

def run(screen):
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 150)

    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu'

        keys = pygame.key.get_pressed()
        player.update(keys=keys, joystick=joystick)

        screen.fill((180, 80, 150)) 
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
