import pygame
import math

from src.settings import *
from src.utility import normalize, clamp
from src.physics.colliders import CircleCollider
from src.physics.collision_system import collision_manager
from src.physics.vectors import Vector2
from src.physics.transform import Transform
from src.render import surface_manager

from src.entities.entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__(Transform(Vector2(*CENTER)))  # теперь используем transform
        self.vx, self.vy = 0.0, 0.0
        self.r = PLAYER_RADIUS
        self.dash_cd = 0.0
        self.dash_t = 0.0
        self.alive = True
        self.focus = FOCUS_MAX * 0.6
        self.tags = ["player"]

        self.collider = CircleCollider(
            owner=self,
            radius=self.r,
            group="player",
            mask=["enemy", "orb", "echo"],  # с кем взаимодействует
            touchable=True
        )
        collision_manager.register(self.collider)

    def input(self, keys):
        ax = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        ay = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        dx, dy = normalize(ax, ay)
        speed = PLAYER_SPEED
        if self.dash_t > 0.0:
            speed = DASH_SPEED
        self.vx, self.vy = dx * speed, dy * speed

    def update(self, dt):
        self.dash_cd = max(0.0, self.dash_cd - dt)
        self.dash_t = max(0.0, self.dash_t - dt)
        # двигаем transform.position
        self.transform.position.x += self.vx * dt
        self.transform.position.y += self.vy * dt
        # ограничение по границам
        self.transform.position.x = clamp(self.transform.position.x, self.r, WIDTH - self.r)
        self.transform.position.y = clamp(self.transform.position.y, self.r, HEIGHT - self.r)

    def try_dash(self):
        if self.dash_cd <= 0.0:
            self.dash_t = DASH_DURATION
            self.dash_cd = DASH_COOLDOWN

    def draw(self, surf):

        x = int(self.transform.position.x)
        y = int(self.transform.position.y)
        # основной круг игрока
        pygame.draw.circle(surf, PLAYER_COLOR, (x, y), self.r)
        # dash cooldown ring
        cd_ratio = 1.0 - clamp(self.dash_cd / DASH_COOLDOWN, 0.0, 1.0)
        pygame.draw.circle(surf, WHITE, (x, y), self.r + 6, 2)
        end_angle = -math.pi / 2 + cd_ratio * 2 * math.pi
        pygame.draw.arc(surf, ECHO_COLOR, (x - self.r - 6, y - self.r - 6, (self.r + 6) * 2, (self.r + 6) * 2), -math.pi/2, end_angle, 3)
        # focus halo
        focus_ratio = clamp(self.focus / FOCUS_MAX, 0.0, 1.0)
        if focus_ratio > 0:
            pygame.draw.circle(surf, FOCUS_COLOR, (x, y), int(self.r + 10 + 6 * focus_ratio), 1)
