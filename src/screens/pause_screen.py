import pygame

class PauseScreen:
    def __init__(self, screen, width=400, height=250):
        self.screen = screen
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 36)

        self.rect = pygame.Rect(
            (self.screen.get_width() - self.width) // 2,
            (self.screen.get_height() - self.height) // 2,
            self.width,
            self.height
        )

        self.btn_continue_rect = pygame.Rect(
            self.rect.left + 100,
            self.rect.top + 70,
            200,
            40
        )
        self.btn_level_select_rect = pygame.Rect(
            self.rect.left + 100,
            self.rect.top + 120,
            200,
            40
        )
        self.btn_menu_rect = pygame.Rect(
            self.rect.left + 100,
            self.rect.top + 170,
            200,
            40
        )

    def draw(self):
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(230)
        s.fill((0, 0, 0))
        self.screen.blit(s, (self.rect.left, self.rect.top))

        text = self.font.render("PAUSA", True, (255, 255, 0))
        text_x = self.rect.left + (self.width - text.get_width()) // 2
        text_y = self.rect.top + 20
        self.screen.blit(text, (text_x, text_y))

        pygame.draw.rect(self.screen, (70, 130, 180), self.btn_continue_rect)
        continue_text = self.button_font.render("Continuar", True, (255, 255, 255))
        continue_x = self.btn_continue_rect.centerx - continue_text.get_width() // 2
        continue_y = self.btn_continue_rect.centery - continue_text.get_height() // 2
        self.screen.blit(continue_text, (continue_x, continue_y))

        pygame.draw.rect(self.screen, (70, 130, 180), self.btn_level_select_rect)
        level_select_text = self.button_font.render("Selección de niveles", True, (255, 255, 255))
        level_select_x = self.btn_level_select_rect.centerx - level_select_text.get_width() // 2
        level_select_y = self.btn_level_select_rect.centery - level_select_text.get_height() // 2
        self.screen.blit(level_select_text, (level_select_x, level_select_y))

        pygame.draw.rect(self.screen, (70, 130, 180), self.btn_menu_rect)
        menu_text = self.button_font.render("Menú", True, (255, 255, 255))
        menu_x = self.btn_menu_rect.centerx - menu_text.get_width() // 2
        menu_y = self.btn_menu_rect.centery - menu_text.get_height() // 2
        self.screen.blit(menu_text, (menu_x, menu_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.btn_continue_rect.collidepoint(mouse_pos):
                return 'continue'
            elif self.btn_level_select_rect.collidepoint(mouse_pos):
                return 'level_select'
            elif self.btn_menu_rect.collidepoint(mouse_pos):
                return 'menu'
        return None
