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
        position = self.transform.position
        player = GameManager.game.player
        player_position = player.transform.position
        dx, dy = player_position.x - position.x, player_position.y - position.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed
        position.x += self.vx * dt
        position.y += self.vy * dt

    def draw(self, surf):
        position = self.transform.position
        pygame.draw.circle(surf, self.color, (int(position.x), int(position.y)), self.r)
        # small eye
        pygame.draw.circle(surf, BLACK, (int(position.x), int(position.y)), 3)

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
        position = self.transform.position
        position.x += self.vx * dt
        position.y += self.vy * dt

        # Удаляем врага, если он улетел далеко за экран
        margin = 100  # запас за пределами экрана
        if (position.x < -margin or position.x > WIDTH + margin or
                position.y < -margin or position.y > HEIGHT + margin):
            self.destroy()

    def start(self):
        position = self.transform.position
        player = GameManager.game.player
        player_position = player.transform.position
        dx, dy = player_position.x - position.x, player_position.y - position.y
        ndx, ndy = normalize(dx, dy)
        self.vx, self.vy = ndx * self.speed, ndy * self.speed

    def destroy(self):
        GameManager.destroy_me(entity=self)
