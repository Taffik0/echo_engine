import random
import pygame

from src.settings import *
from src.utility import normalize, clamp
from src.game_manager import GameManager
from src.entities.entity import Entity
from src.physics.colliders import Collider
from src.physics.colision_manager import collision_manager


class Enemy(Entity):
    standard_speed_boost = 1
    color = ENEMY_COLOR
    x = 0
    y = 0

    def __init__(self, speed_boost=0.0):
        self.r = ENEMY_RADIUS
        # Spawn from a random edge and move towards a drifting target near player to avoid predictability

        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX + speed_boost) * self.standard_speed_boost
        self.vx, self.vy = 0.0, 0.0

        self.collider = Collider(
            owner=self,
            radius=self.r,
            group="enemy",
            mask=["player"]  # с кем взаимодействует
        )
        collision_manager.register(self.collider)

    def update(self, dt):
        player = GameManager.game.player
        dx, dy = player.x - self.x, player.y - self.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.r)
        # small eye
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), 3)

    def start(self):
        pass

    def on_collision(self, other):
        print("столкнулся", other, self)
        GameManager.game.end_game()


class FastEnemy(Enemy):
    standard_speed_boost = 4
    color = (100, 60, 100)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Удаляем врага, если он улетел далеко за экран
        margin = 50  # запас за пределами экрана
        if (self.x < -margin or self.x > WIDTH + margin or
                self.y < -margin or self.y > HEIGHT + margin):
            self.destroy()

    def start(self):
        player = GameManager.game.player
        dx, dy = player.x - self.x, player.y - self.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed

    def destroy(self):
        GameManager.destroy_me(entity=self, entity_type="enemy")
