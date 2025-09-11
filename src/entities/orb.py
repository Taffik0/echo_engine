import random
import math
import pygame

from src.settings import *

from src.entities.entity import Entity

from src.physics.colliders import Collider
from src.physics.colision_manager import collision_manager
from src.game_manager import GameManager


class Orb(Entity):
    def __init__(self):
        margin = 30
        self.x = random.uniform(margin, WIDTH - margin)
        self.y = random.uniform(margin, HEIGHT - margin)
        self.r = ORB_RADIUS
        self.t = 0.0
        self.life = ORB_LIFETIME

        self.collider = Collider(
            owner=self,
            radius=self.r,
            group="orb",
            mask=["player"]  # с кем взаимодействует
        )
        collision_manager.register(self.collider)

    def update(self, dt):
        self.t += dt

    def alive(self):
        return self.t < self.life

    def draw(self, surf):
        # pulsing ring
        pygame.draw.circle(surf, ORB_COLOR, (int(self.x), int(self.y)), self.r)
        pulse = 2 + int(2 * math.sin(self.t * 6))
        pygame.draw.circle(surf, ORB_COLOR, (int(self.x), int(self.y)), self.r + 6 + pulse, 1)

    def on_collision(self, other):
        GameManager.game.absorb_echoes()
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self, "orb")
