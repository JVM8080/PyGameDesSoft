import pygame

def level_select(screen):
    pygame.mixer.init()  
    pygame.mixer.music.load("assets/sounds/gravity_falls_abertura1.mp3")
    pygame.mixer.music.play()  
    font = pygame.font.SysFont(None, 50)

    background = pygame.image.load("assets/images/menu/level select.png").convert()
    background = pygame.transform.scale(background, screen.get_size())

    button_images = [
        pygame.image.load("assets/images/menu/level 1.png").convert_alpha(),
        pygame.image.load("assets/images/menu/level 2.png").convert_alpha(),
        pygame.image.load("assets/images/menu/level 3.png").convert_alpha()
    ]
    button_images = [pygame.transform.scale(img, (180, 60)) for img in button_images]

    positions = [(80, 430), (300, 400), (520, 370)]  # x, y de cada botão

    level_buttons = []
    for i, img in enumerate(button_images):
        rect = img.get_rect(topleft=positions[i])
        level_buttons.append(rect)

    while True:
        screen.blit(background, (0, 0))

        for i, rect in enumerate(level_buttons):
            screen.blit(button_images[i], rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(event.pos):
                        return 'game', i + 1

        pygame.display.flip()
