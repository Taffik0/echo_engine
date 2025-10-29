import math
from math import sqrt
from src.physics.vectors import Vector2, Vector2N
from typing import Tuple, Optional


def aabb_penetration(ax: float, ay: float, aw: float, ah: float,
                     bx: float, by: float, bw: float, bh: float
                     ) -> Tuple[bool, Optional[Vector2], float]:
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
        return True, normal, penetration
    return False, None, 0.0


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


def circle_rect_penetration(circle_pos: Vector2, circle_radius: float,
                            rect_x: float, rect_y: float,
                            rect_width: float, rect_height: float) -> Tuple[bool, Optional[Vector2], float]:
    cx, cy = circle_pos.x, circle_pos.y

    # ближайшая точка на прямоугольнике к центру круга
    nearest_x = max(rect_x, min(cx, rect_x + rect_width))
    nearest_y = max(rect_y, min(cy, rect_y + rect_height))

    # вектор от ближайшей точки к центру круга
    dx = cx - nearest_x
    dy = cy - nearest_y
    dist_sq = dx*dx + dy*dy

    # если центр круга внутри прямоугольника
    inside = False
    if cx > rect_x and cx < rect_x + rect_width and cy > rect_y and cy < rect_y + rect_height:
        inside = True

    if dist_sq > circle_radius**2 and not inside:
        return False, Vector2(0, 0), 0.0  # столкновения нет

    # вычисляем глубину проникновения
    if inside:
        # выбираем минимальное смещение, чтобы выйти наружу
        left = cx - rect_x
        right = rect_x + rect_width - cx
        top = cy - rect_y
        bottom = rect_y + rect_height - cy

        min_dist = min(left, right, top, bottom)
        if min_dist == left:
            normal = Vector2(-1, 0)
            penetration = left + circle_radius
        elif min_dist == right:
            normal = Vector2(1, 0)
            penetration = right + circle_radius
        elif min_dist == top:
            normal = Vector2(0, -1)
            penetration = top + circle_radius
        else:
            normal = Vector2(0, 1)
            penetration = bottom + circle_radius
    else:
        distance = sqrt(dist_sq)
        normal = Vector2(dx / distance, dy / distance)  # нормаль от rect к кругу
        penetration = circle_radius - distance

    return True, normal, penetration


class Projection:
    def __init__(self, min_x: float, max_x: float):
        self.min_x = min_x
        self.max_x = max_x
        self.collider = None  # позже заполним в sweep_and_prune