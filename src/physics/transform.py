from .physics import Vector2


class Transform:
    def __init__(self, position: Vector2 = Vector2(0, 0), rotation: Vector2 = Vector2(0, 0),
                 size: Vector2 = Vector2(1, 1), is_sizing=True):
        self.position: Vector2 = position
        self.size: Vector2 = size
        self.rotation: Vector2 = rotation
        self.is_sizing = is_sizing
