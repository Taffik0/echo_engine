import pygame
from collections import deque

from src.settings import *
from src.utility import clamp
from src.physics.colision_manager import collision_manager

from src.entities.player import Player
from src.sound_manager import SoundManager
from src.event_system import EventSystem

from src.spawners import spawner_register
from src.workers import worker_register


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadow Echo — Endless Mini-Arcade")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 48, bold=True)

        self.player = None
        self.entities = []
        self.running = False
        self.game_over = False
        self.time = 0.0
        self.score = 0.0
        self.high = 0

        EventSystem.trigger_event("start")

    def reset(self):
        collision_manager.reset()

        self.player = Player()
        self.entities = []
        self.running = True
        self.game_over = False
        self.time = 0.0
        self.score = 0.0
        self.high = self.load_highscore()

        spawner_register.reset_spawners()
        worker_register.reset_workers()

        SoundManager.load_and_run_sound(path="../assets/music/untitled.mp3", loops=-1)

    def load_highscore(self):
        try:
            with open("../shadow_echo_highscore.txt", "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_highscore(self):
        try:
            with open("../shadow_echo_highscore.txt", "w") as f:
                f.write(str(self.high))
        except Exception:
            pass

    def update(self, dt, slow_factor):
        if self.game_over:
            return
        self.time += dt

        # Player update
        self.player.update(dt)
        self.score += 60*dt  # slow earn when time-slow active

        # Entity update
        for e in self.entities:
            e.update(dt * slow_factor)

        spawner_register.spawners_update(dt*slow_factor)
        worker_register.workers_update(dt)

        collision_manager.check_all()

    def end_game(self):
        self.game_over = True
        self.high = max(self.high, int(self.score))
        self.save_highscore()

    def draw_grid(self, surf):
        gap = 30
        for x in range(0, WIDTH, gap):
            pygame.draw.line(surf, (30, 32, 36), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, gap):
            pygame.draw.line(surf, (30, 32, 36), (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)

        for en in self.entities:
            en.draw(self.screen)

        self.player.draw(self.screen)

        # UI
        bar_w, bar_h = 180, 10
        # focus bar
        pygame.draw.rect(self.screen, (40, 60, 80), (15, 15, bar_w, bar_h), border_radius=6)
        ratio = clamp(self.player.focus / FOCUS_MAX, 0.0, 1.0)
        pygame.draw.rect(self.screen, FOCUS_COLOR, (15, 15, int(bar_w * ratio), bar_h), border_radius=6)
        self.screen.blit(self.font.render("FOCUS", True, WHITE), (15, 28))

        # score
        self.screen.blit(self.font.render(f"Score: {int(self.score)}", True, WHITE), (WIDTH - 170, 12))
        self.screen.blit(self.font.render(f"Best:  {self.high}", True, GRAY), (WIDTH - 170, 32))

        if self.game_over:
            s1 = self.big_font.render("GAME OVER", True, WHITE)
            s2 = self.font.render("R - restart    ESC - quit", True, GRAY)
            s3 = self.font.render("Tip: Grab green orbs to cash-in echoes!", True, GRAY)
            self.screen.blit(s1, (CENTER[0] - s1.get_width()//2, CENTER[1] - 60))
            self.screen.blit(s2, (CENTER[0] - s2.get_width()//2, CENTER[1]))
            self.screen.blit(s3, (CENTER[0] - s3.get_width()//2, CENTER[1] + 26))

        pygame.display.flip()

    def run(self):
        slow_factor = 1.0
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_SPACE and not self.game_over:
                        self.player.try_dash()

            keys = pygame.key.get_pressed()
            if not self.game_over:
                self.player.input(keys)

            # Focus slow-time (hold SHIFT)
            slow_factor = 1.0
            if not self.game_over and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                if self.player.focus > 0:
                    slow_factor = MIN_SLOW
                    self.player.focus = clamp(self.player.focus - FOCUS_DRAIN * dt, 0, FOCUS_MAX)
            else:
                self.player.focus = clamp(self.player.focus + FOCUS_REGEN * dt, 0, FOCUS_MAX)

            self.update(dt, slow_factor)
            self.draw()
        pygame.quit()
