import pygame
from src.objects.animation import Portal
from config import *

def carregar_imagem_totem():
    totem_sheet = pygame.image.load("assets/images/level2/totem.png").convert_alpha()
    totem = Portal(
        x=400,  # Posição X fixa
        y=HEIGHT - 250,  # Posição Y fixa
        spritesheet=totem_sheet,
        frame_width=totem_sheet.get_width()//7,
        frame_height=totem_sheet.get_height(),
        frame_count=7,
        frame_speed=100,
        scale_size = (120,140)
    )
    return totem

def carregar_imagem_fogo():
    fogo_sheet = pygame.image.load("assets/images/level2/fogo.png").convert_alpha()
    fire = Portal(
        x=WIDTH/2-115,
        y=HEIGHT - 215,
        spritesheet=fogo_sheet,
        frame_width=fogo_sheet.get_width()//8,
        frame_height=fogo_sheet.get_height(),
        frame_count=8,
        frame_speed=100,
        scale_size=(230, 230)
    )
    return fire