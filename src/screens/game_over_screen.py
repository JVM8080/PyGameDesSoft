import pygame

class GameOverScreen:
    def __init__(self, screen, width=400, height=200):
        self.screen = screen
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 40)

        self.rect = pygame.Rect(
            (self.screen.get_width() - self.width) // 2,
            (self.screen.get_height() - self.height) // 2,
            self.width,
            self.height
        )

        # Botones dentro del cuadro
        self.btn_reset_rect = pygame.Rect(
            self.rect.left + 50,
            self.rect.top + 120,
            120,
            40
        )
        self.btn_menu_rect = pygame.Rect(
            self.rect.left + 230,
            self.rect.top + 120,
            120,
            40
        )

    def draw(self):
        
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(220)  
        s.fill((0, 0, 0))
        self.screen.blit(s, (self.rect.left, self.rect.top))

        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        text_x = self.rect.left + (self.width - game_over_text.get_width()) // 2
        text_y = self.rect.top + 40
        self.screen.blit(game_over_text, (text_x, text_y))

        
        pygame.draw.rect(self.screen, (100, 100, 100), self.btn_reset_rect)
        reset_text = self.button_font.render("Reiniciar", True, (255, 255, 255))
        reset_x = self.btn_reset_rect.centerx - reset_text.get_width() // 2
        reset_y = self.btn_reset_rect.centery - reset_text.get_height() // 2
        self.screen.blit(reset_text, (reset_x, reset_y))

        pygame.draw.rect(self.screen, (100, 100, 100), self.btn_menu_rect)
        menu_text = self.button_font.render("Salir al Menú", True, (255, 255, 255))
        menu_x = self.btn_menu_rect.centerx - menu_text.get_width() // 2
        menu_y = self.btn_menu_rect.centery - menu_text.get_height() // 2
        self.screen.blit(menu_text, (menu_x, menu_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.btn_reset_rect.collidepoint(mouse_pos):
                return 'reset'
            elif self.btn_menu_rect.collidepoint(mouse_pos):
                return 'menu'
        return None
