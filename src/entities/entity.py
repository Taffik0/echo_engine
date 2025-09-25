from src.game_manager import GameManager
import pygame

from src.physics.physics import Vector2


class Entity:

    def __init__(self):
        self.tags = ["entity"]
        self.entity_name = ""
        self.collider = None
        self.color = (0, 0, 0)
        self.visible = True
        self.position = Vector2()

    def update(self, dt):
        pass

    def draw(self, surf):
        pass

    def start(self):
        pass

    def destroy(self):
        pass

    def on_collision(self, other):
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
        GameManager.spawn_entity(self.entity, self.entity_type, self.position.x, self.position.y)
