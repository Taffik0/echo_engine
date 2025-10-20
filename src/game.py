import inspect
import pygame

from src.settings import *
from src.utility import clamp
from src.physics.collision_system import collision_manager
from src.physics.physics_system import PhysicsSystem
from src.systems.modifier.modifier_system import ModifierSystem

from src.entities.player import Player
from src.render.camera import Camera
from src.render.canvas import Canvas
from src.sound_manager import SoundManager
from src.systems.event_system import EventSystem

from src.spawners import spawner_register
from src.workers import worker_register
from src.visual_effects.visual_effects_registr import VisualEffectRegister

from src.physics.transform import Transform, TransformUI
from src.physics.vectors import Vector2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadow Echo — Endless Mini-Arcade")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)

        self.player = None
        self.entities = []
        self.camera = Camera(Transform(size=Vector2(900, 600)), 1)
        self.canvases = [Canvas(Transform(size=Vector2(900, 600)), 1)]
        self.running = True
        self.game_over = False
        self.time = 0.0

    def reset(self):
        print("reset")
        collision_manager.reset()

        self.player = Player()
        self.entities = []
        self.camera = Camera(Transform(size=Vector2(900, 600)), 1)
        self.canvases = [Canvas(Transform(size=Vector2(900, 600)), 1)]
        self.running = True
        self.game_over = False
        self.time = 0.0

        spawner_register.reset_spawners()
        worker_register.reset_workers()

        SoundManager.load_and_run_sound(path="assets/music/untitled.wav", loops=-1)
        EventSystem.trigger_event("reset")


    def update(self, dt, slow_factor):
        if self.game_over:
            return
        self.time += dt
        ModifierSystem.update(dt)
        # Player update
        self.player.update(dt)

        # Entity update
        for e in self.entities:
            e.update(dt * slow_factor)

        PhysicsSystem.update_all(dt*slow_factor)

        EventSystem.trigger_event("update")  # call update event

        spawner_register.spawners_update(dt*slow_factor)
        worker_register.workers_update(dt)

        collision_manager.check_all()
        EventSystem.trigger_event("lastUpdate") # call lastUpdate event

    def end_game(self):
        self.game_over = True
        stack = inspect.stack()
        caller = stack[1]  # [0] — это текущий кадр, [1] — кто вызвал
        print(f"Игра закончена от: {caller.function}, в файле: {caller.filename}, строка: {caller.lineno}")
        print(self.entities)
        EventSystem.trigger_event("end_game")

    def draw(self, dt, slow_factor):
        self.screen.fill(BLACK)
        VisualEffectRegister.under_draw(self.screen, dt*slow_factor)

        for en in self.entities:
            result = en.draw(self.screen)
            if result is None:
                continue  # ничего не рисуем
            # Если draw вернул только Surface
            if isinstance(result, pygame.Surface):
                surface = result
                self.camera.add_to_draw_queue(surface, en)
            # Если draw вернул (Surface, alignment)
            elif isinstance(result, tuple):
                surface, alignment = result
                self.camera.add_to_draw_queue(surface, en, alignment=alignment)

        self.camera.drawing_queue(self.screen)

        self.player.draw(self.screen)

        VisualEffectRegister.draw(self.screen, dt*slow_factor)

        for canvas in self.canvases:
            canvas.add_to_draw_queue_all_ui()
            canvas.drawing_queue(self.screen)
        # UI
        bar_w, bar_h = 180, 10
        # focus bar
        pygame.draw.rect(self.screen, (40, 60, 80), (15, 15, bar_w, bar_h), border_radius=6)
        ratio = clamp(self.player.focus / FOCUS_MAX, 0.0, 1.0)
        pygame.draw.rect(self.screen, FOCUS_COLOR, (15, 15, int(bar_w * ratio), bar_h), border_radius=6)
        self.screen.blit(self.font.render("FOCUS", True, WHITE), (15, 28))

        VisualEffectRegister.over_draw(self.screen, dt*slow_factor)

        pygame.display.flip()

    def start(self):
        EventSystem.trigger_event("init")
        EventSystem.trigger_event("start")

    def run(self):
        slow_factor = 1.0
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(f"entity in game {len(self.entities)}")
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print(f"entity in game {len(self.entities)}")
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
            self.draw(dt, slow_factor)
        pygame.quit()
