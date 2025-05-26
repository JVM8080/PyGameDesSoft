import pygame
import os
from config import WIDTH, HEIGHT
from pygame import mixer

def tela_vitoria(screen):
    VITORIA_SOUND = mixer.Sound("assets/sounds/resultados/victory.wav")
    VITORIA_SOUND.set_volume(0.6)
    VITORIA_SOUND.play(loops=-1)

    # Carregar os frames da animação
    frames = []
    folder = "assets/images/level2/gif.winner"
    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            frames.append(img)

    frame_index = 0
    frame_speed = 150  # milissegundos por frame
    last_update = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'

        now = pygame.time.get_ticks()
        if now - last_update > frame_speed:
            frame_index = (frame_index + 1) % len(frames)
            last_update = now

        screen.blit(frames[frame_index], (0, 0))
        pygame.display.flip()
        clock.tick(60)
