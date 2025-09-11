import pygame
import math

from src.settings import *
from src.utility import normalize, clamp
from src.physics.colliders import Collider
from src.physics.colision_manager import collision_manager

from src.entities.entity import Entity


class Player(Entity):
    def __init__(self):
        self.x, self.y = CENTER
        self.vx, self.vy = 0.0, 0.0
        self.r = PLAYER_RADIUS
        self.dash_cd = 0.0
        self.dash_t = 0.0
        self.alive = True
        self.focus = FOCUS_MAX * 0.6

        self.collider = Collider(
            owner=self,
            radius=self.r,
            group="player",
            mask=["enemy", "orb", "echo"]  # с кем взаимодействует
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
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = clamp(self.x, self.r, WIDTH - self.r)
        self.y = clamp(self.y, self.r, HEIGHT - self.r)

    def try_dash(self):
        if self.dash_cd <= 0.0:
            self.dash_t = DASH_DURATION
            self.dash_cd = DASH_COOLDOWN

    def draw(self, surf):
        # Ring indicates dash cooldown, blue ring indicates focus reserve
        pygame.draw.circle(surf, PLAYER_COLOR, (int(self.x), int(self.y)), self.r)
        # dash ring
        cd_ratio = 1.0 - clamp(self.dash_cd / DASH_COOLDOWN, 0.0, 1.0)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.r + 6, 2)
        end_angle = -math.pi / 2 + cd_ratio * 2 * math.pi
        pygame.draw.arc(surf, ECHO_COLOR, (self.x - self.r - 6, self.y - self.r - 6, (self.r + 6) * 2, (self.r + 6) * 2), -math.pi/2, end_angle, 3)
        # focus halo
        focus_ratio = clamp(self.focus / FOCUS_MAX, 0.0, 1.0)
        if focus_ratio > 0:
            pygame.draw.circle(surf, FOCUS_COLOR, (int(self.x), int(self.y)), int(self.r + 10 + 6 * focus_ratio), 1)
