import pygame
import math

from src.render import surface_manager
import src.settings as settings  # ← правильный импорт настроек
from src.utility import normalize, clamp
from src.physics.colliders import CircleCollider
from src.physics.collision_system import collision_manager
from src.physics.vectors import Vector2
from src.physics.transform import Transform
from src.game_manager import GameManager

from src.entities.entity import Entity

from src.systems.user_imput.user_input_system import UserInputSystem, KeyEvent


class Player(Entity):
    def __init__(self):
        super().__init__(Transform(Vector2(*settings.CENTER)))  # НОВОЕ: settings.CENTER
        self.vx, self.vy = 0.0, 0.0
        self.r = settings.PLAYER_RADIUS
        self.dash_cd = 0.0
        self.dash_t = 0.0
        self.alive = True
        self.focus = settings.FOCUS_MAX * 0.6
        self.tags = ["player"]

        self.collider = CircleCollider(
            owner=self,
            radius=self.r,
            group="player",
            mask=["enemy", "orb", "echo"],
            touchable=True
        )
        collision_manager.register(self.collider)
        UserInputSystem.registration_event(KeyEvent(44, self.try_dash, on_down=True))

    def input(self):
        keys = pygame.key.get_pressed()
        ax = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        ay = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        dx, dy = normalize(ax, ay)

        speed = settings.PLAYER_SPEED
        if self.dash_t > 0.0:
            speed = settings.DASH_SPEED

        self.vx, self.vy = dx * speed, dy * speed

    def update(self, dt):
        dt = dt / GameManager.game.slow_factor
        self.dash_cd = max(0.0, self.dash_cd - dt)
        self.dash_t = max(0.0, self.dash_t - dt)

        # движение
        self.transform.position.x += self.vx * dt
        self.transform.position.y += self.vy * dt

        # ограничение по границам (теперь корректно обновляется)
        cam = GameManager.game.camera.transform
        self.transform.position.x = clamp(self.transform.position.x, cam.position.x + self.r,
                                          cam.position.x + cam.size.x - self.r)
        self.transform.position.y = clamp(self.transform.position.y, cam.position.y + self.r,
                                          cam.position.y + cam.size.y - self.r)

        self.input()

    def try_dash(self):
        if self.dash_cd <= 0.0:
            self.dash_t = settings.DASH_DURATION
            self.dash_cd = settings.DASH_COOLDOWN

    def draw(self, surf):
        if not self.visible:
            return

        # Surface под рисование
        surface = surface_manager.create_surface_by_circle(self.r + 16)

        cx = self.r + 16
        cy = self.r + 16

        # основной круг
        pygame.draw.circle(surface, settings.PLAYER_COLOR, (cx, cy), self.r)

        # cooldown круг
        cd_ratio = 1.0 - clamp(self.dash_cd / settings.DASH_COOLDOWN, 0.0, 1.0)
        pygame.draw.circle(surface, settings.WHITE, (cx, cy), self.r + 6, 2)

        end_angle = -math.pi / 2 + cd_ratio * 2 * math.pi
        pygame.draw.arc(
            surface,
            settings.ECHO_COLOR,
            (cx - (self.r + 6), cy - (self.r + 6), (self.r + 6) * 2, (self.r + 6) * 2),
            -math.pi / 2,
            end_angle,
            3
        )

        # focus halo
        focus_ratio = clamp(self.focus / settings.FOCUS_MAX, 0.0, 1.0)
        if focus_ratio > 0:
            pygame.draw.circle(
                surface,
                settings.FOCUS_COLOR,
                (cx, cy),
                int(self.r + 10 + 6 * focus_ratio),
                1
            )

        return surface
