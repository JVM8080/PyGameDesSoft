import pygame
import sys
from config import *
from src.screens.main_menu import main_menu
from src.screens.level_select import level_select
from src.screens.game_screen import game_screen

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGameDesSoft")
clock = pygame.time.Clock()

state = 'menu'
selected_level = 1

while True:
    if state == 'menu':
        state = main_menu(screen)
    elif state == 'level_select':
        state, selected_level = level_select(screen)
    elif state == 'game':
        state = game_screen(screen, selected_level)
    elif state == 'quit':
        pygame.quit()
        sys.exit()

    clock.tick(FPS)
