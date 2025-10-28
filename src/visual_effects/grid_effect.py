import pygame

from src.settings import WIDTH, HEIGHT

from .visual_effect import VisualEffect
from .visual_effects_register import VisualEffectRegister


class GridEffect(VisualEffect):
    def draw(self, surface, dt):
        gap = 30
        for x in range(0, WIDTH, gap):
            pygame.draw.line(surface, (30, 32, 36), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, gap):
            pygame.draw.line(surface, (30, 32, 36), (0, y), (WIDTH, y))

