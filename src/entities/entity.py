from src.game_manager import GameManager
import pygame
from  pygame import Surface

from src.physics.vectors import Vector2
from src.physics.transform import Transform

from .entity_data import EntityData


class Entity(EntityData):
    pass


class LifeTimeEntity(Entity):

    def __init__(self, life_time):
        super().__init__()
        self.life_time = life_time
        self.start_life_time = life_time
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.life_time:
            self.on_life_time_end()

    def on_life_time_end(self):
        pass


class EntitySpawner(LifeTimeEntity):
    def __init__(self, life_time, entity, entity_type):
        super().__init__(life_time)
        self.entity = entity
        self.entity_type = entity_type

    def on_life_time_end(self):
        GameManager.spawn_entity(self.entity(), position=self.transform.position)
