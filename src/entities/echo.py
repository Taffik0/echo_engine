import pygame

from src.settings import *

from src.utility import clamp


class Echo:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.r = ECHO_RADIUS
        self.t = 0.0
        self.life = ECHO_LIFETIME

    def update(self, dt):
        self.t += dt

    def alive(self):
        return self.t < self.life

    def draw(self, surf):
        # fade out
        a = 1.0 - clamp(self.t / self.life, 0.0, 1.0)
        col = (int(ECHO_COLOR[0] * a + BLACK[0] * (1-a)), int(ECHO_COLOR[1] * a + BLACK[1] * (1-a)), int(ECHO_COLOR[2] * a + BLACK[2] * (1-a)))
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.r, 2)