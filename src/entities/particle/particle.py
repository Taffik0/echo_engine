import random

from src.physics.physics import Vector2
from src.game_manager import GameManager

from src.entities.entity import EntitySpawner, LifeTimeEntity


class Particle(LifeTimeEntity):
    def __init__(self, life_time, color, r, speed: Vector2):
        super().__init__(life_time)
        self.color = color
        self.r = r
        self.speed = speed

        self.tags = ["particle"]

    def update(self, dt):
        super().update(dt)
        self.x += self.speed.x
        self.y += self.speed.y

    def on_life_time_end(self):
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self)


class ParticleSpawner(EntitySpawner):

    def __init__(self, entity: Particle, frequency, r, particle_color, particle_r,
                 entity_speed_min: Vector2, entity_speed_max: Vector2,
                 entity_life_time_min, entity_life_time_max,
                 entity_type="entity"):
        super().__init__(frequency, entity, entity_type)
        self.r = r
        self.entity_speed_min = entity_speed_min
        self.entity_speed_max = entity_speed_max
        self.entity_life_time_min = entity_life_time_min
        self.entity_life_time_max = entity_life_time_max
        self.particle_color = particle_color
        self.particle_r = particle_r

    def on_life_time_end(self):
        self.life_time = self.start_life_time
        particle_life_time = random.uniform(self.entity_life_time_min, self.entity_life_time_max)
        particle_speed = Vector2(
            random.uniform(self.entity_speed_min.x, self.entity_speed_max.x),
            random.uniform(self.entity_speed_min.y, self.entity_speed_max.y)
        )
        particle_r = self.particle_r
        particle_color = self.particle_color
        particle = self.entity(particle_life_time, particle_color, particle_r, particle_speed
                               )
