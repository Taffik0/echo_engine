from .colliders import Collider

from .vectors import Vector2


class CollisionManager:
    def __init__(self):
        self.colliders: list[Collider] = []

    def register(self, collider):
        self.colliders.append(collider)

    def unregister(self, collider):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def check_all(self):
        colliders_copy = list(self.colliders)
        for i in range(len(colliders_copy)):
            for j in range(i + 1, len(colliders_copy)):
                c1 = colliders_copy[i]
                c2 = colliders_copy[j]
                if not self.check_projection(c1, c2, axis="x"):
                    continue
                if not self.check_projection(c1, c2, axis="y"):
                    continue
                if c1 in self.colliders and c2 in self.colliders: # оба ещё живы
                    is_collision, normal, penetration = c1.check_collision(c2)
                    if is_collision:
                        c1.owner.on_collision(c2.owner)
                        c2.owner.on_collision(c1.owner)
                        if c1.touchable and c2.touchable:
                            self.collision_normal(c1, c2, normal, penetration)

    def collision_normal(self, c1: Collider, c2: Collider, normal: Vector2, penetration: float):
        c1.owner.transform.position += normal * penetration/2
        c2.owner.transform.position -= normal * penetration / 2

    def check_projection(self, c1: Collider, c2: Collider, axis="x"):
        c1_min, c1_max = c1.get_projection(axis)
        c2_min, c2_max = c2.get_projection(axis)
        return (c1_min <= c2_max) and (c1_max >= c2_min)

    def reset(self):
        self.colliders = []


collision_manager = CollisionManager()
