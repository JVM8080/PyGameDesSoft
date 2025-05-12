import pygame
from config import IMG_PATH

_cache = {}

def load_image(name, size=None):
    key = (name, size)

    if key not in _cache:
        image = pygame.image.load(IMG_PATH + name).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        _cache[key] = image

    return _cache[key]
