from .entity import LifeTimeEntity

from src.physics.physics import Vector2
from src.game_manager import GameManager


class Particle(LifeTimeEntity):
    def __init__(self, life_time, speed: Vector2, color, r):
        super().__init__(life_time)
        self.speed = speed
        self.color = color
        self.r = r

    def update(self, dt):
        self.x += self.speed.x
        self.y += self.speed.y

    def on_life_time_end(self):
        self.destroy()

    def destroy(self):
        GameManager.destroy_me(self, "entity")