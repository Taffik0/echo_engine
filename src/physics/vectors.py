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

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # Умножение на число
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            # Покомпонентное умножение
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return NotImplemented

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    # длина и нормализация
    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return self / l if l != 0 else Vector2(0, 0)

    def normalize_ip(self):
        l = self.length()
        if l != 0:
            self.x /= l
            self.y /= l
        return self

    # скалярное произведение
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # превращение в tuple (для pygame)
    def to_tuple(self):
        return (int(self.x), int(self.y))


class Vector2N(Vector2):
    def __init__(self,  x: float = 0.0, y: float = 0.0, n_for_max: bool = False, n_for_sum: bool = False):
        super().__init__(x, y)
        if n_for_max:
            self.normalized_for_max()
        elif n_for_sum:
            self.normalized_for_sum()
        elif x != 0 or y != 0:
            self.normalize_ip()

    def normalized_for_sum(self):
        v_sum = self.x + self.y
        if v_sum != 0:
            self.x = self.x / v_sum
            self.y = self.y / v_sum

    def normalized_for_max(self):
        v_max = max((self.x, self.y))
        if v_max != 0:
            self.x = self.x / v_max
            self.y = self.y / v_max
