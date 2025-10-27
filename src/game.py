import inspect
import pygame
import sdl2
import sdl2.ext

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
from src.systems.user_imput.user_input_system import UserInputSystem

from src.spawners import spawner_register
from src.workers.worker_register import WorkerRegister
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

        self.player = Player()
        self.entities = []
        self.camera = Camera(Transform(size=Vector2(900, 600)), 1)
        self.canvases = [Canvas(Transform(size=Vector2(900, 600)), 1)]
        self.running = True
        self.game_over = False
        self.time = 0.0
        self.slow_factor = 1.0

        WorkerRegister.init_workers()

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
        self.slow_factor = 1.0

        spawner_register.reset_spawners()
        WorkerRegister.reset_workers()

        EventSystem.trigger_event("reset")

    def update(self, dt):
        slow_factor = self.slow_factor
        UserInputSystem.update(dt)
        if self.game_over:
            return
        self.time += dt
        ModifierSystem.update(dt)
        # Player update
        self.player.update(dt*slow_factor)

        # Entity update
        for e in self.entities:
            e.update(dt * slow_factor)

        PhysicsSystem.update_all(dt*slow_factor)

        EventSystem.trigger_event("update")  # call update event

        spawner_register.spawners_update(dt*slow_factor)
        WorkerRegister.workers_update(dt)

        collision_manager.check_all()
        EventSystem.trigger_event("lastUpdate") # call lastUpdate event

    def end_game(self):
        self.game_over = True
        stack = inspect.stack()
        caller = stack[1]  # [0] — это текущий кадр, [1] — кто вызвал
        print(f"Игра закончена от: {caller.function}, в файле: {caller.filename}, строка: {caller.lineno}")
        print(self.entities)
        EventSystem.trigger_event("end_game")
        print(f"entity in game {len(self.entities)}")

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

        VisualEffectRegister.over_draw(self.screen, dt*slow_factor)

        pygame.display.flip()

    def start(self):
        EventSystem.trigger_event("init")
        EventSystem.trigger_event("start")

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.end_game()
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset()
            self.update(dt)
            self.draw(dt, self.slow_factor)
        pygame.quit()
