import inspect
import pygame
from src.settings import *
from src.systems.modifier.modifier_system import ModifierSystem
from src.systems.logger import Logger

from src.systems.event_system import EventSystem
from src.systems.user_imput.user_input_system import UserInputSystem

from src.workers.worker_register import WorkerRegister

from .scene.scene import Scene
from .scene.scene_init import scenes_init, worker_scenes_init

from src.utils.class_holder import SceneHolder


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shadow Echo — Endless Mini-Arcade")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.scenes_prefab: list[SceneHolder] = []
        self.scenes_loaded: list[Scene] = []
        self.active_scene: Scene | None = None

        self.running = True
        self.game_over = False
        self.time = 0.0
        self.slow_factor = 1.0

        WorkerRegister.init_workers()

    def reset(self):
        Logger.info("reset")

        self.running = True
        self.game_over = False
        self.time = 0.0
        self.slow_factor = 1.0

        WorkerRegister.reset_workers()

        EventSystem.trigger_event("reset")

    def update(self, dt):
        active_scene = self.active_scene
        slow_factor = self.slow_factor

        UserInputSystem.update(dt)

        if self.game_over:
            return
        self.time += dt
        ModifierSystem.update(dt)
        # Player update
        if active_scene.player:
            active_scene.player.update(dt*slow_factor)

        # Entity update
        for e in active_scene.entities:
            e.update(dt * slow_factor)

        # PhysicsSystem.update_all(dt*slow_factor)
        active_scene.physics_system.update_all(dt*slow_factor)

        EventSystem.trigger_event("update")  # call update event
        active_scene.event_system.trigger_event("update")

        WorkerRegister.workers_update(dt)
        active_scene.worker_register.workers_update(dt)

        EventSystem.trigger_event("lastUpdate")  # call lastUpdate event
        active_scene.event_system.trigger_event("lastUpdate")

    def exit(self):
        self.running = False

    def end_game(self):
        self.game_over = True
        stack = inspect.stack()
        caller = stack[1]  # [0] — это текущий кадр, [1] — кто вызвал
        EventSystem.trigger_event("end_game")
        Logger.info(f"Игра закончена от: {caller.function}, в файле: {caller.filename}, строка: {caller.lineno}")
        Logger.info(f"{self.active_scene.entities}")
        Logger.info(f"entity in game {len(self.active_scene.entities)}")

    def draw(self, dt, slow_factor):
        active_scene = self.active_scene
        self.screen.fill(BACKGROUND_COLOR)

        active_scene.visual_effects_register.under_draw(self.screen, dt*slow_factor)

        for en in active_scene.entities:
            result = en.draw(self.screen)
            if result is None:
                continue  # ничего не рисуем
            # Если draw вернул только Surface
            if isinstance(result, pygame.Surface):
                surface = result
                active_scene.camera.add_to_draw_queue(surface, en)
            # Если draw вернул (Surface, alignment)
            elif isinstance(result, tuple):
                surface, alignment = result
                active_scene.camera.add_to_draw_queue(surface, en, alignment=alignment)

        active_scene.camera.drawing_queue(self.screen)

        if active_scene.player:
            active_scene.player.draw(self.screen)

        active_scene.visual_effects_register.draw(self.screen, dt*slow_factor)

        for canvas in active_scene.canvases:
            canvas.add_to_draw_queue_all_ui()
            canvas.drawing_queue(self.screen)

        active_scene.visual_effects_register.over_draw(self.screen, dt*slow_factor)

        pygame.display.flip()

    def start(self):
        EventSystem.trigger_event("init")
        self.scenes_prefab = scenes_init()
        worker_scenes_init({scene.name: scene for scene in self.scenes_prefab})
        if not self.scenes_prefab:
            Logger.error("can't run - no scenes")
            return
        self.scenes_loaded.append(self.scenes_prefab[0].create_instance())
        self.active_scene = self.scenes_loaded[0]
        EventSystem.trigger_event("start")
        self.active_scene.event_system.trigger_event("start")
        self.run()

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
