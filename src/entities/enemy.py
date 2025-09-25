import random
import pygame

from src.settings import *
from src.utility import normalize, clamp
from src.game_manager import GameManager
from src.entities.entity import Entity
from src.physics.colliders import CircleCollider
from src.physics.colision_manager import collision_manager


class Enemy(Entity):
    def __init__(self, speed_boost=0.0):
        super().__init__()
        self.r = ENEMY_RADIUS
        self.tags = ["enemy"]
        self.standard_speed_boost = 1
        self.color = ENEMY_COLOR

        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX + speed_boost) * self.standard_speed_boost
        self.vx, self.vy = 0.0, 0.0

        self.collider = CircleCollider(
            owner=self,
            radius=self.r,
            group="enemy",
            mask=["player"]  # с кем взаимодействует
        )
        collision_manager.register(self.collider)

    def update(self, dt):
        player = GameManager.game.player
        dx, dy = player.x - self.position.x, player.y - self.position.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed
        self.position.x += self.vx * dt
        self.position.y += self.vy * dt

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.position.x), int(self.position.y)), self.r)
        # small eye
        pygame.draw.circle(surf, BLACK, (int(self.position.x), int(self.position.y)), 3)

    def start(self):
        pass

    def on_collision(self, other):
        GameManager.game.end_game()


class FastEnemy(Enemy):
    def __init__(self, speed_boost=0.0):
        super().__init__(speed_boost)
        self.color = (100, 60, 100)
        self.standard_speed_boost = 6

        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX + speed_boost) * self.standard_speed_boost

    def update(self, dt):
        self.position.x += self.vx * dt
        self.position.y += self.vy * dt

        # Удаляем врага, если он улетел далеко за экран
        margin = 100  # запас за пределами экрана
        if (self.position.x < -margin or self.position.x > WIDTH + margin or
                self.position.y < -margin or self.position.y > HEIGHT + margin):
            self.destroy()

    def start(self):
        player = GameManager.game.player
        dx, dy = player.x - self.position.x, player.y - self.position.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed

    def destroy(self):
        GameManager.destroy_me(entity=self)
