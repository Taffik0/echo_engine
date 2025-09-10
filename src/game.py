import pygame
import random
import math
from collections import deque

from settings import *
from utility import clamp, circle_hit
from src.game_manager import GameManager
from src.factories.enemy_factory import EnemyFactory

from entities.player import Player
from entities.enemy import Enemy
from entities.echo import Echo
from entities.orb import Orb

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadow Echo — Endless Mini-Arcade")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 48, bold=True)

        self.player = None
        self.enemies = []
        self.echoes = []
        self.orbs = []
        self.running = False
        self.game_over = False
        self.time = 0.0
        self.score = 0
        self.high = 0
        self.t_enemy = 0.0
        self.t_echo = 0.0
        self.t_orb = 0.0
        self.t_diff = 0.0
        self.echo_delay = 0.0
        self.enemy_spawn = 0.0
        self.enemy_speed_boost = 0.0
        self.orb_spawn = 0.0
        self.trail = deque()
        self.trail_gap = 0
        self.trail_countdown = 0

    def reset(self):
        self.player = Player()
        self.enemies = []
        self.echoes = []
        self.orbs = []
        self.running = True
        self.game_over = False
        self.time = 0.0
        self.score = 0
        self.high = self.load_highscore()
        # Timers
        self.t_enemy = 0.0
        self.t_echo = 0.0
        self.t_orb = 0.0
        self.t_diff = 0.0
        # Difficulty state
        self.echo_delay = ECHO_SPAWN_DELAY
        self.enemy_spawn = ENEMY_SPAWN_EVERY
        self.enemy_speed_boost = 0.0
        self.orb_spawn = ORB_SPAWN_EVERY
        # Trail buffer to place echoes from historical positions
        self.trail = deque(maxlen=int(FPS * 3))  # store last ~3 seconds positions
        self.trail_gap = int(self.echo_delay * FPS)
        self.trail_countdown = self.trail_gap

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

    def spawn_enemy(self):
        EnemyFactory.create_enemy(self.enemy_speed_boost)

    def spawn_orb(self):
        self.orbs.append(Orb())

    def absorb_echoes(self):
        absorbed = len(self.echoes)
        self.score += absorbed * 5
        self.echoes.clear()
        # small reward: burst of focus
        self.player.focus = clamp(self.player.focus + 30, 0, FOCUS_MAX)

    def update(self, dt, slow_factor):
        if self.game_over:
            return
        self.time += dt
        self.t_enemy += dt
        self.t_echo += dt
        self.t_orb += dt
        self.t_diff += dt

        # Difficulty scaling
        if self.t_diff >= DIFF_EVERY:
            self.t_diff = 0.0
            self.echo_delay *= DIFF_ECHO_DELAY_MULT
            self.enemy_spawn *= DIFF_ENEMY_RATE_MULT
            self.enemy_speed_boost += DIFF_ENEMY_SPEED_ADD
            self.orb_spawn *= DIFF_ORB_RATE_MULT
            self.trail_gap = max(4, int(self.echo_delay * FPS))

        # Player update
        self.player.update(dt)
        self.score += int(1 * slow_factor)  # slow earn when time-slow active
        # Enemies
        if self.t_enemy >= self.enemy_spawn:
            self.t_enemy = 0.0
            self.spawn_enemy()
        for e in self.enemies:
            e.update(dt * slow_factor)

        # Trail and echo spawning from trail history
        self.trail.append((self.player.x, self.player.y))
        self.trail_countdown -= 1
        if self.trail_countdown <= 0 and len(self.trail) > 0:
            self.trail_countdown = self.trail_gap
            tx, ty = self.trail[0]
            self.echoes.append(Echo(tx, ty))

        # Update echoes
        for ec in self.echoes:
            ec.update(dt * slow_factor)
        self.echoes = [ec for ec in self.echoes if ec.alive()]

        # Orbs
        if self.t_orb >= self.orb_spawn:
            self.t_orb = 0.0
            self.spawn_orb()
        for o in self.orbs:
            o.update(dt * slow_factor)
        self.orbs = [o for o in self.orbs if o.alive()]

        # Collisions
        # Enemies with player
        for e in self.enemies:
            if circle_hit(self.player.x, self.player.y, self.player.r, e.x, e.y, e.r):
                self.end_game()
                return
        # Echoes with player
        for ec in self.echoes:
            if circle_hit(self.player.x, self.player.y, self.player.r, ec.x, ec.y, ec.r):
                self.end_game()
                return
        # Orbs with player
        for o in list(self.orbs):
            if circle_hit(self.player.x, self.player.y, self.player.r, o.x, o.y, o.r):
                self.orbs.remove(o)
                self.absorb_echoes()

    def end_game(self):
        self.game_over = True
        self.high = max(self.high, self.score)
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

        # Draw echoes beneath enemies
        for ec in self.echoes:
            ec.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        for o in self.orbs:
            o.draw(self.screen)
        self.player.draw(self.screen)

        # UI
        bar_w, bar_h = 180, 10
        # focus bar
        pygame.draw.rect(self.screen, (40, 60, 80), (15, 15, bar_w, bar_h), border_radius=6)
        ratio = clamp(self.player.focus / FOCUS_MAX, 0.0, 1.0)
        pygame.draw.rect(self.screen, FOCUS_COLOR, (15, 15, int(bar_w * ratio), bar_h), border_radius=6)
        self.screen.blit(self.font.render("FOCUS", True, WHITE), (15, 28))

        # score
        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (WIDTH - 170, 12))
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
