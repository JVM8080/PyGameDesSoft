import pygame

def level_select(screen):
    font = pygame.font.SysFont(None, 50)
    level_buttons = [pygame.Rect(150 + i * 170, 250, 150, 60) for i in range(3)]

    while True:
        screen.fill((50, 50, 50))

        for i, rect in enumerate(level_buttons):
            pygame.draw.rect(screen, (100, 180, 100), rect)
            text = font.render(f"Nivel {i+1}", True, (0, 0, 0))
            screen.blit(text, (rect.x + 25, rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(event.pos):
                        return 'game', i + 1

        pygame.display.flip()
