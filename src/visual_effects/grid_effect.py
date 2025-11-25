import pygame

import src.settings as settings

from .visual_effect import VisualEffect
from .visual_effects_registr import VisualEffectRegister


class GridEffect(VisualEffect):
    def draw(self, surface, dt):
        gap = 30
        for x in range(0, settings.WIDTH, gap):
            pygame.draw.line(surface, (30, 32, 36), (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, gap):
            pygame.draw.line(surface, (30, 32, 36), (0, y), (settings.WIDTH, y))


grid_effect = GridEffect()
VisualEffectRegister.add(grid_effect, -1)
