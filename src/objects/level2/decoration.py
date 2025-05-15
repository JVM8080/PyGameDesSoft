import pygame
from kill_reset import Portal
from config import *

totem_sheet = pygame.image.load("assets/images/level2/totem.png").convert_alpha()
totem = Portal(
    x=400,
    y=HEIGHT - 250,
    spritesheet=totem_sheet,
    frame_width=131,
    frame_height=197,
    frame_count=8,
    frame_speed=100 )