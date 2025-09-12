import math


class Vector2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    # арифметика
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    # длина и нормализация
    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return self / l if l != 0 else Vector2(0, 0)

    # скалярное произведение
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # превращение в tuple (для pygame)
    def to_tuple(self):
        return (int(self.x), int(self.y))