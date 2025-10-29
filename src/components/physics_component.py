from .component import Component

from src.physics.physics_body import PhysicsBody

from src.physics.vectors import Vector2
from src.managers.physics_manager import PhysicsManager


class PhysicsComponent(Component):
    def __init__(self, mass: float, velocity: Vector2 = Vector2(0, 0), 
                 acceleration: Vector2 = Vector2(0, 0),
                 forces: list[Vector2] = None, is_static: bool = False, *args, **kwargs):
        super().__init__(**kwargs)
        self.physics_body = PhysicsBody(owner=self.owner, mass=mass, velocity=velocity,
                                        acceleration=acceleration,
                                        forces=forces, is_static=is_static)

    def start(self):
        self.physics_body.owner = self.owner
        PhysicsManager.register(self.physics_body)

    def on_delete(self):
        PhysicsManager.unregister(self.physics_body)
