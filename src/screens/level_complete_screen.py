import pygame
from config import WIDTH, HEIGHT

class LevelCompleteScreen:
    def __init__(self, screen, width=400, height=200):
        self.screen = screen
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(None, 48) 
        self.button_font = pygame.font.SysFont(None, 36)

        # Rectángulo central para el panel
        self.rect = pygame.Rect(
            (self.screen.get_width() - self.width) // 2,
            (self.screen.get_height() - self.height) // 2,
            self.width,
            self.height
        )

        # Botones dentro del cuadro
        self.btn_restart_rect = pygame.Rect(
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
        # Crear superficie semitransparente para el panel
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(220)  # Nivel de transparencia (0-255)
        s.fill((0, 0, 0))  # Color negro semitransparente
        self.screen.blit(s, (self.rect.left, self.rect.top))

        # Dibujar borde del panel
        pygame.draw.rect(self.screen, (255, 215, 0), self.rect, 3)

        title_text = self.font.render("Level Complete!", True, (255, 215, 0))  
        text_x = self.rect.left + (self.width - title_text.get_width()) // 2
        text_y = self.rect.top + 40
        self.screen.blit(title_text, (text_x, text_y))

        pygame.draw.rect(self.screen, (50, 150, 50), self.btn_restart_rect)
        restart_text = self.button_font.render("Restart", True, (255, 255, 255))
        restart_x = self.btn_restart_rect.centerx - restart_text.get_width() // 2
        restart_y = self.btn_restart_rect.centery - restart_text.get_height() // 2
        self.screen.blit(restart_text, (restart_x, restart_y))

        pygame.draw.rect(self.screen, (150, 50, 50), self.btn_menu_rect) 
        menu_text = self.button_font.render("Menu", True, (255, 255, 255))
        menu_x = self.btn_menu_rect.centerx - menu_text.get_width() // 2
        menu_y = self.btn_menu_rect.centery - menu_text.get_height() // 2
        self.screen.blit(menu_text, (menu_x, menu_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.btn_restart_rect.collidepoint(mouse_pos):
                return 'restart'
            elif self.btn_menu_rect.collidepoint(mouse_pos):
                return 'menu'
        return None