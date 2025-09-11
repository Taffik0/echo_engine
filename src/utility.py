import math


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def vec_length(x, y):
    return math.hypot(x, y)


def normalize(x, y):
    l = vec_length(x, y)
    if l == 0:
        return 0.0, 0.0
    return x / l, y / l


def circle_hit(ax, ay, ar, bx, by, br):
    return (ax - bx) ** 2 + (ay - by) ** 2 <= (ar + br) ** 2


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
