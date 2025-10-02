from src.physics.transform import Transform


class VisualEffect:
    def __init__(self, transform: Transform = None):
        self.transform = transform
        if not transform:
            self.transform = Transform()

    def draw(self, surface, dt):
        pass