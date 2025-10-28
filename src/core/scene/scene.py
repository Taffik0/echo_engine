from src.systems.event_system import LocalEventSystem
from src.physics.collision_system import CollisionSystem
from src.physics.physics_system import PhysicsSystem
from src.visual_effects.visual_effects_register import VisualEffectRegister
from src.workers.local_worker_reister import LocalWorkerRegister
from src.spawners.spawner_register import SpawnersRegister

from src.physics.transform import Transform, Vector2

from src.render.camera import Camera
from src.render.canvas import Canvas

from src.entities.entity_data import EntityData


class Scene:
    def __init__(self):
        self.event_system: LocalEventSystem = LocalEventSystem()
        self.collision_system: CollisionSystem = CollisionSystem()
        self.physics_system: PhysicsSystem = PhysicsSystem()
        self.camera: Camera = Camera(Transform(size=Vector2(900, 600)), 1)
        self.canvases: list[Canvas] = [Canvas(Transform(size=Vector2(900, 600)), 1)]
        self.entities: list[EntityData] = []
        self.player = None
        self.visual_effects_register: VisualEffectRegister = VisualEffectRegister()
        self.worker_register: LocalWorkerRegister = LocalWorkerRegister()
        self.spawner_register: SpawnersRegister = SpawnersRegister()
