import pygame

from src.settings import *

from src.utility import clamp
from src.physics.colliders import CircleCollider
from src.physics.colision_manager import collision_manager
from src.entities.entity import LifeTimeEntity, EntitySpawner
from src.game_manager import GameManager


class Echo(LifeTimeEntity):
    def __init__(self, x, y):
        super().__init__(ECHO_LIFETIME)
        self.x, self.y = x, y
        self.r = ECHO_RADIUS
        self.tags = ["echo"]

        self.collider = CircleCollider(
            owner=self,
            radius=self.r,
            group="echo",
            mask=["player"]  # с кем взаимодействует
        )
        collision_manager.register(self.collider)

    def alive(self):
        return self.current_time < self.life_time

    def draw(self, surf):
        # fade out
        progress = self.current_time / self.life_time
        a = clamp((1.0 - progress*0.5), lo=0.0, hi=0.5)
        col = (
            int(ECHO_COLOR[0] - ECHO_COLOR[0]*(1-a)),
            int(ECHO_COLOR[1] - ECHO_COLOR[1]*(1-a)),
            int(ECHO_COLOR[2] - ECHO_COLOR[2]*(1-a))
        )
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), self.r, 2)

    def on_collision(self, other):
        GameManager.destroy_me(self)
        GameManager.game.end_game()

    def on_life_time_end(self):
        GameManager.destroy_me(self)


class EchoSpawner(EntitySpawner):
    def __init__(self, life_time, entity, entity_type):
        super().__init__(life_time, entity, entity_type)

        self.color = (40, 40, 100)
        self.r = 7

    def draw(self, surf):
        if not self.visible:
            return
        pygame.draw.circle(surf, self.color, (int(self.position.x), int(self.position.y)), self.r, 2)

    def on_life_time_end(self):
        super().on_life_time_end()
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self)
