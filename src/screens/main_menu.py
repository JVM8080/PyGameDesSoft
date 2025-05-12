import pygame

def main_menu(screen):
    font = pygame.font.SysFont(None, 60)
    button_rect = pygame.Rect(300, 250, 200, 60)

    while True:
        screen.fill((30, 30, 30))
        text = font.render("START", True, (255, 255, 255))
        pygame.draw.rect(screen, (70, 70, 200), button_rect)
        screen.blit(text, (button_rect.x + 40, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return 'level_select'

        pygame.display.flip()
