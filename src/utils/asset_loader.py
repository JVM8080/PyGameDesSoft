import pygame
from config import IMG_PATH

_cache = {}

def load_image(name, size=None):
    key = (name, size)

    if key not in _cache:
        image = pygame.image.load(IMG_PATH + name).convert_alpha()

        if size:
            width, height = size

            if height == "auto":
                original_width, original_height = image.get_size()
                scale_factor = width / original_width
                height = int(original_height * scale_factor)

            image = pygame.transform.scale(image, (width, height))

        _cache[key] = image

    return _cache[key]