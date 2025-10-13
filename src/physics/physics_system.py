from typing import List

from .vectors import Vector2

from .physics_body import PhysicsBody


class PhysicsSystem:
    physics_bodies: list[PhysicsBody] = []

    @classmethod
    def register(cls, physics_body):
        cls.physics_bodies.append(physics_body)

    @classmethod
    def unregister(cls, physics_body):
        if physics_body in cls.physics_bodies:
            cls.physics_bodies.remove(physics_body)


    @classmethod
    def update_all(cls, dt):
        for pb in cls.physics_bodies:
            if pb.is_static:
                continue
            if pb.mass == 0:
                continue
            force = sum(pb.forces, Vector2(0, 0))
            pb.acceleration = force / pb.mass
            pb.velocity += pb.acceleration * dt
            pb.owner.transform.position += pb.velocity * dt
            pb.forces.clear()
