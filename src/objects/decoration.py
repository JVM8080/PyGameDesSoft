import pygame
from src.objects.animation import Portal
from config import *

def carregar_imagem_totem():
    totem_sheet = pygame.image.load("assets/images/level2/totem.png").convert_alpha()
    totem = Portal(
        x=400,
        y=HEIGHT - 250,
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
        x=WIDTH/2 - 115,
        y=HEIGHT - 215,
        spritesheet=fogo_sheet,
        frame_width=fogo_sheet.get_width() // 8,
        frame_height=fogo_sheet.get_height(),
        frame_count=8,
        frame_speed=100,
        scale_size=(230, 230)
    )
    fire.hitbox = pygame.Rect(WIDTH//2 - 40, HEIGHT - 120, 80, 80)
    return fire

vida_img = None
POS_VIDAS = (20, 20)

def desenhar_vidas(surface, vidas):
    global vida_img
    if vida_img is None:
        vida_img = pygame.image.load("assets/images/level2/vidas.png").convert_alpha()
        vida_img = pygame.transform.scale(vida_img, (280,40))

    total_coracoes = 10
    coracao_largura = vida_img.get_width() // total_coracoes
    coracao_altura = vida_img.get_height()

    largura_mostrar = max(0, vidas) * coracao_largura
    rect = pygame.Rect(0, 0, largura_mostrar, coracao_altura)
    surface.blit(vida_img, POS_VIDAS, rect)

