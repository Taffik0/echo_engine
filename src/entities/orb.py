import random
import math
import pygame

from src.settings import *

from src.entities.entity import Entity, LifeTimeEntity

from src.physics.colliders import CircleCollider
from src.physics.colision_manager import collision_manager
from src.game_manager import GameManager


class Orb(LifeTimeEntity):
    def __init__(self):
        super().__init__(ORB_LIFETIME)
        self.r = ORB_RADIUS

        self.collider = CircleCollider(
            owner=self,
            radius=self.r,
            group="orb",
            mask=["player"]  # с кем взаимодействует
        )
        collision_manager.register(self.collider)

    def update(self, dt):
        super().update(dt)

    def alive(self):
        return self.current_time < self.life_time

    def draw(self, surf):
        # pulsing ring
        pygame.draw.circle(surf, ORB_COLOR, (int(self.transform.position.x), int(self.transform.position.y)), self.r)
        pulse = 2 + int(2 * math.sin(self.current_time * 6))
        pygame.draw.circle(surf, ORB_COLOR, (int(self.transform.position.x), int(self.transform.position.y)), self.r + 6 + pulse, 1)

    def on_collision(self, other):
        echos = GameManager.get_entity_by_tag("echo")
        GameManager.hard_remove_list(echos, "echo")
        GameManager.destroy_me(self)

    def on_life_time_end(self):
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self)
