from src.utility import singleton


class CollisionManager:
    def __init__(self):
        self.colliders = []

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
                if c1 in self.colliders and c2 in self.colliders:  # оба ещё живы
                    if c1.check_collision(c2):
                        c1.owner.on_collision(c2.owner)
                        c2.owner.on_collision(c1.owner)

    def reset(self):
        self.colliders = []


collision_manager = CollisionManager()
