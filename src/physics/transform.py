from .vectors import Vector2, Vector2N


class Transform:
    def __init__(self, position: Vector2 = Vector2(0, 0), rotation: Vector2 = Vector2(0, 0),
                 size: Vector2 = Vector2(1, 1), is_sizing=True):
        self.position: Vector2 = position
        self.size: Vector2 = size
        self.rotation: Vector2 = rotation
        self.is_sizing = is_sizing


class TransformUI:
    def __init__(self, position: Vector2 = Vector2(0, 0), rotation: Vector2 = Vector2(0, 0),
                 relative_position: Vector2N = Vector2N(0, 0),
                 size_px: Vector2 = Vector2(1, 1), is_sizing=True,
                 relative_size: Vector2N = Vector2N(0, 0),
                 alignment: str = "ld", draw_alignment="ld"):

        self.position: Vector2 = position
        self.relative_position = relative_position
        self.size_px: Vector2 = size_px
        self.rotation: Vector2 = rotation
        self.is_sizing = is_sizing
        self.relative_size = relative_size
        self.alignment = alignment
        self.draw_alignment = draw_alignment

