from .vectors import Vector2
from src.entities.entity import EntityData


class PhysicsBody:
    def __init__(self, owner: EntityData, mass: float, velocity: Vector2 = Vector2(0, 0), acceleration: Vector2 = Vector2(0, 0),
                 forces: list[Vector2] = None, is_static: bool = False):
        self.owner = owner
        self.mass: float = mass
        self.velocity: Vector2 = velocity
        self.acceleration: Vector2 = acceleration
        if forces:
            self.forces: list[Vector2] = forces
        else:
            self.forces: list[Vector2] = []
        self.is_static: bool = is_static

    def apply_force(self, force):
        self.forces.append(force)
