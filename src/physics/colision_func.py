import math
from src.physics.vectors import Vector2, Vector2N
from typing import Tuple, Optional


def aabb_penetration(ax: float, ay: float, aw: float, ah: float,
                     bx: float, by: float, bw: float, bh: float
                     ) -> Tuple[Optional[Vector2], float]:
    """
    ax,ay = левый верхний угол (или любой corner), aw = width, ah = height
    Возвращает (normal, penetration) или (None, 0) если нет пересечения.
    normal направлен от B к A (чтобы вытолкнуть A наружу).
    """
    # центры
    a_cx = ax + aw / 2
    a_cy = ay + ah / 2
    b_cx = bx + bw / 2
    b_cy = by + bh / 2

    dx = b_cx - a_cx
    dy = b_cy - a_cy

    overlap_x = (aw / 2 + bw / 2) - abs(dx)
    overlap_y = (ah / 2 + bh / 2) - abs(dy)

    if overlap_x > 0 and overlap_y > 0:
        # есть пересечение — берем минимальную глубину
        if overlap_x < overlap_y:
            # коррекция по X
            normal = Vector2(1 if dx > 0 else -1, 0)
            penetration = overlap_x
        else:
            # коррекция по Y
            normal = Vector2(0, 1 if dy > 0 else -1)
            penetration = overlap_y
        return normal, penetration
    return None, 0.0


def circle_penetration(c1_pos, c1_radius, c2_pos, c2_radius) -> Tuple[bool, Optional[Vector2], float]:
    dx = c2_pos.x - c1_pos.x
    dy = c2_pos.y - c1_pos.y
    distance = math.hypot(dx, dy)
    penetration = c1_radius + c2_radius - distance
    normal = Vector2()
    if distance == 0:
        # если центры совпали, выбираем произвольное направление
        normal = Vector2(1, 0)
    else:
        normal = Vector2N(dx, dy)
    return penetration if penetration > 0 else 0, normal, penetration


class Projection:
    def __init__(self, min_x: float, max_x: float):
        self.min_x = min_x
        self.max_x = max_x
        self.collider = None  # позже заполним в sweep_and_prune