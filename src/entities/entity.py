from src.game_manager import GameManager
import pygame

from src.physics.physics import Vector2
from src.physics.transform import Transform


class Entity:

    def __init__(self, transform: Transform = None):
        self.tags = ["entity"]
        self.entity_name = ""
        self.collider = None
        self.color = (0, 0, 0)
        self.visible = True
        self.transform: Transform = transform if transform is not None else Transform()
        self.components = {}

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

    def add_component(self, component):
        self.components[type(component)] = component

    def has_component(self, comp_type):
        return comp_type in self.components

    def get_component(self, comp_type):
        return self.components.get(comp_type, None)


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
