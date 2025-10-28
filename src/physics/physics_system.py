from typing import List

from .vectors import Vector2

from .physics_body import PhysicsBody


class PhysicsSystem:
    def __init__(self):
        self.physics_bodies: list[PhysicsBody] = []

    def register(self, physics_body):
        self.physics_bodies.append(physics_body)

    def unregister(self, physics_body):
        if physics_body in self.physics_bodies:
            self.physics_bodies.remove(physics_body)

    def update_all(self, dt):
        for pb in self.physics_bodies:
            if pb.is_static:
                continue
            if pb.mass == 0:
                continue
            force = sum(pb.forces, Vector2(0, 0))
            pb.acceleration = force / pb.mass
            pb.velocity += pb.acceleration * dt
            pb.owner.transform.position += pb.velocity * dt
            pb.forces.clear()
