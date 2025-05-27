import pygame
import sys
from config import *
from src.screens.main_menu import main_menu
from src.screens.level_select import level_select
from src.screens.game_screen import game_screen

# Inicializa todos os módulos do Pygame
pygame.init()

# Cria a janela do jogo com as dimensões definidas em WIDTH e HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define o título da janela
pygame.display.set_caption("PyGameDesSoft")

# Cria um objeto Clock para controlar os frames por segundo (FPS)
clock = pygame.time.Clock()

# Inicializa o módulo de joystick
pygame.joystick.init()

# Verifica se há algum joystick conectado
if pygame.joystick.get_count() > 0:
    # Pega o primeiro joystick disponível
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick conectado:", joystick.get_name())
else:
    joystick = None
    print("No hay joystick conectado")

# Define o estado inicial como o menu principal
state = 'menu'

# Define o nível selecionado como 1 por padrão
selected_level = 1

# Loop principal do jogo
while True:
    # Verifica o estado atual e executa a função correspondente
    if state == 'menu':
        state = main_menu(screen)
    elif state == 'level_select':
        state, selected_level = level_select(screen)
    elif state == 'game':
        state = game_screen(screen, selected_level)
    elif state == 'quit':
        # Sai do jogo corretamente
        pygame.quit()
        sys.exit()

    # Controla o FPS do jogo com base na configuração
    clock.tick(FPS)
