import pygame
from config import IMG_PATH

_cache = {}

def load_image(name, size=None):
    key = (name, size)

    if key not in _cache:
        image = pygame.image.load(IMG_PATH + name).convert_alpha()

        if size:
            width, height = size
            original_width, original_height = image.get_size()

            if height == "auto":
                scale_factor = width / original_width
                height = int(original_height * scale_factor)

            elif width == "auto":
                scale_factor = height / original_height
                width = int(original_width * scale_factor)

            image = pygame.transform.scale(image, (width, height))

        _cache[key] = image

    return _cache[key]