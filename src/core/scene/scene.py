from src.systems.event_system import LocalEventSystem
from src.physics.collision_system import CollisionSystem
from src.physics.physics_system import PhysicsSystem
from src.visual_effects.visual_effects_register import VisualEffectRegister
from src.workers.local_worker_register import LocalWorkerRegister
from src.spawners.spawner_register import SpawnersRegister
from src.systems.global_variables.local_global_variables_system import LocalGlobalVariablesSystem
from src.systems.user_imput.local_user_input_system import LocalUserInputSystem

from src.physics.transform import Transform, Vector2

from src.render.camera import Camera
from src.render.canvas import Canvas

from src.entities.entity_data import EntityData

from src.systems.logger import Logger


class Scene:
    def __init__(self, name: str = None, workers:
                 list = None, spawners: list = None, entities: list = None, visual_effects: list = None):
        if name:
            self.name = name
        else:
            Logger.error(f"scene can't haven't name {self}")
            return
        self.event_system: LocalEventSystem = LocalEventSystem()
        self.collision_system: CollisionSystem = CollisionSystem()
        self.physics_system: PhysicsSystem = PhysicsSystem()
        self.global_variable_system: LocalGlobalVariablesSystem = LocalGlobalVariablesSystem(f"scene_{self.name}")
        self.user_input_system: LocalUserInputSystem = LocalUserInputSystem()

        self.camera: Camera = Camera(Transform(size=Vector2(900, 600)), 1)
        self.canvases: list[Canvas] = [Canvas(Transform(size=Vector2(900, 600)), 1)]

        self.entities: list[EntityData] = []
        if entities:
            self.entities = entities
        self.player = None

        self.visual_effects_register: VisualEffectRegister = VisualEffectRegister()
        self.worker_register: LocalWorkerRegister = LocalWorkerRegister()
        self.spawner_register: SpawnersRegister = SpawnersRegister()

        if workers:
            for worker in workers:
                self.worker_register.add_worker_prefab(worker)

        if spawners:
            for spawner in spawners:
                self.spawner_register.add_spawner(spawner)

        if visual_effects:
            for ve, level in visual_effects:
                self.visual_effects_register.add(ve, level)

        self.worker_register.init_workers()

        self.event_system.trigger_event("init")

    def load(self):
        Logger.debug(f"Scene {self.name} loaded")

    def unload(self):
        Logger.debug(f"Scene {self.name} unloaded")
        self.user_input_system.keys = []
