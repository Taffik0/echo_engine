import random
import math
import pygame

from src.render import surface_manager
from src.settings import *

from src.entities.entity import Entity, LifeTimeEntity

from src.physics.colliders import CircleCollider
from src.physics.collision_system import collision_manager
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
        if not self.visible:
            return

        # создаём surface с запасом для пульсающего кольца
        surface = surface_manager.create_surface_by_circle(self.r + 10)

        cx = self.r + 10
        cy = self.r + 10

        # основной шар
        pygame.draw.circle(surface, ORB_COLOR, (cx, cy), self.r)

        # пульсирующее кольцо
        pulse = 2 + int(2 * math.sin(self.current_time * 6))
        pygame.draw.circle(surface, ORB_COLOR, (cx, cy), self.r + 6 + pulse, 1)

        return surface

    def on_collision(self, other):
        echos = GameManager.get_entity_by_tag("echo")
        GameManager.hard_remove_list(echos, "echo")
        GameManager.destroy_me(self)

    def on_life_time_end(self):
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self)
