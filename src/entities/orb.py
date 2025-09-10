import random
import math
import pygame

from src.settings import *


class Orb:
    def __init__(self):
        margin = 30
        self.x = random.uniform(margin, WIDTH - margin)
        self.y = random.uniform(margin, HEIGHT - margin)
        self.r = ORB_RADIUS
        self.t = 0.0
        self.life = ORB_LIFETIME

    def update(self, dt):
        self.t += dt

    def alive(self):
        return self.t < self.life

    def draw(self, surf):
        # pulsing ring
        pygame.draw.circle(surf, ORB_COLOR, (int(self.x), int(self.y)), self.r)
        pulse = 2 + int(2 * math.sin(self.t * 6))
        pygame.draw.circle(surf, ORB_COLOR, (int(self.x), int(self.y)), self.r + 6 + pulse, 1)