import pygame
from src.utils.asset_loader import load_image
from pygame import mixer



def main_menu(screen):

    mixer.music.load("assets/sounds/menu/introducao.ogg")
    mixer.music.set_volume(0.6)
    mixer.music.play(-1)  # -1 = loop infinito

    clock = pygame.time.Clock()

    # Fundo do menu
    background = load_image("inicio_menu.jpg")
    background = pygame.transform.scale(background, screen.get_size())

    # Tentativa de usar uma fonte mais cartunesca
    try:
        font = pygame.font.Font("src/assets/fonts/GravityFalls.ttf", 36)  # Coloque a fonte no caminho indicado
    except:
        font = pygame.font.SysFont("comicsansms", 36)

    white = (255, 255, 255)
    yellow = (255, 255, 0)
    hover_yellow = (255, 255, 102)
    black = (0, 0, 0)

    button_text = "Iniciar Jogo"
    button_rect = pygame.Rect(0, 0, 240, 80)
    button_rect.center = (screen.get_width() // 2, 420)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(mouse_pos):
                    mixer.music.stop()
                    return "level_select"

        screen.blit(background, (0, 0))

        # Animação do botão (efeito hover)
        color = hover_yellow if button_rect.collidepoint(mouse_pos) else yellow
        pygame.draw.rect(screen, color, button_rect, border_radius=12)

        # Sombra
        shadow = font.render(button_text, True, (50, 50, 50))
        screen.blit(shadow, shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2)))

        # Texto do botão
        label = font.render(button_text, True, black)
        screen.blit(label, label.get_rect(center=button_rect.center))

        pygame.display.flip()
        clock.tick(60)
