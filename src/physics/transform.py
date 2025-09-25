from .physics import Vector2


class Transform:
    def __init__(self, position: Vector2, rotation: Vector2, size: Vector2 = Vector2(1, 1), is_sizing = True):
        self.position: Vector2
        self.size: Vector2
        self.rotation: Vector2
        self.is_sizing = True
