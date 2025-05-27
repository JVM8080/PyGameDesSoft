import pygame
from config import *
from pygame import mixer

GAMEOVER_SOUND = None  

def tela_game_over(screen):
    global GAMEOVER_SOUND
    if not GAMEOVER_SOUND:
        GAMEOVER_SOUND = mixer.Sound("assets/sounds/resultados/gameover.ogg")
        GAMEOVER_SOUND.set_volume(SOUND_VOLUME_MUSIC)
    canal_gameover = pygame.mixer.Channel(2)
    canal_gameover.play(GAMEOVER_SOUND, loops=-1)

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
                    canal_gameover.stop()
                    return 'menu'

        screen.blit(gameover_img, (0, 0))
        pygame.display.flip()
        clock.tick(60)
