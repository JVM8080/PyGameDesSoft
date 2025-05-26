import pygame

class PauseScreen:
    def __init__(self, screen, width=450, height=300):
        self.screen = screen
        self.width = width
        self.height = height
        self.active = False

        try:
            self.font = pygame.font.Font("assets/fonts/roboto-bold.ttf", 48)
            self.button_font = pygame.font.Font("assets/fonts/roboto-regular.ttf", 24)
        except:
            self.font = pygame.font.SysFont("Arial", 48, bold=True)
            self.button_font = pygame.font.SysFont("Arial", 24)

        self.rect = self._centered_rect(self.width, self.height)

        self.buttons = {
            'continue': self._create_button("Continuar", 80),
            'level_select': self._create_button("Selecionar Nivel", 140),
            'menu': self._create_button("Menu", 200)
        }

        self.bg_color = (30, 30, 40, 180)  
        self.button_color = (70, 130, 230)
        self.hover_color = (100, 160, 255)
        self.text_color = (255, 255, 255)
        self.title_color = (255, 215, 0)

    def _centered_rect(self, width, height):
        screen_w, screen_h = self.screen.get_size()
        return pygame.Rect(
            (screen_w - width) // 2,
            (screen_h - height) // 2,
            width,
            height
        )

    def _create_button(self, label, offset_y):
        rect = pygame.Rect(
            self.rect.left + (self.width - 220) // 2,
            self.rect.top + offset_y,
            220,
            45
        )
        return {'rect': rect, 'label': label}

    def show(self):
        self.active = True

    def hide(self):
        self.active = False

    def update(self, dt):
        pass  # Sin animaciones

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, self.bg_color, (0, 0, self.width, self.height), border_radius=15)
        
        self.screen.blit(overlay, self.rect.topleft)

        self._draw_title("PAUSA", self.rect.centerx, self.rect.top + 10)

        for btn in self.buttons.values():
            self._draw_button(btn['rect'], btn['label'])

    def _draw_title(self, text, center_x, y):
        main_text = self.font.render(text, True, self.title_color)
        self.screen.blit(main_text, (center_x - main_text.get_width() // 2, y))

    def _draw_button(self, rect, label):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.button_color

        pygame.draw.rect(self.screen, color, rect, border_radius=8)

        text_surface = self.button_font.render(label, True, self.text_color)
        self.screen.blit(text_surface, (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        ))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for action, btn in self.buttons.items():
                if btn['rect'].collidepoint(mouse_pos):
                    return action
        return None