import pygame


def create_surface_by_circle(r):
    return pygame.Surface((r*2, r*2), pygame.SRCALPHA)


def create_surface_by_react(width, height):
    return pygame.Surface((width, height), pygame.SRCALPHA)


def ensure_surface_size(surf, width, height):
    """Расширяет Surface без потери пикселей."""
    w, h = surf.get_size()
    if w >= width and h >= height:
        return surf
    new_w = max(w, width)
    new_h = max(h, height)
    new_surf = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
    new_surf.blit(surf, (0, 0))
    return new_surf
