import math
from typing import Tuple, Optional

from src.physics.vectors import Vector2

from .colision_func import aabb_penetration, circle_penetration, circle_rect_penetration
from src.entities.entity_data import EntityData


class Collider:
    def __init__(self, owner: EntityData, group, mask, active=True, touchable=False):
        self.owner: EntityData = owner
        self.group = group
        self.mask = mask
        self.active = active
        self.touchable = touchable

    def can_collide_with(self, other):
        return other.group in self.mask and self.group in other.mask

    def check_collision(self, other) -> Tuple[bool, Optional[Vector2], float]:
        raise NotImplementedError

    def get_projection(self, axis='x'):
        pass


class CircleCollider(Collider):
    def __init__(self, owner, radius, group, mask, active=True, touchable=False):
        super().__init__(owner, group, mask, active, touchable)
        self.radius = radius

    def check_collision(self, other) -> Tuple[bool, Optional[Vector2], float]:
        if not self.active or not other.active:
            return False, None, 0
        if not self.can_collide_with(other):
            return False, None, 0
        return other.check_collision_with_circle(self)

    def check_collision_with_circle(self, other: "CircleCollider") -> Tuple[bool, Optional[Vector2], float]:
        position = self.owner.transform.position
        other_position = other.owner.transform.position
        return circle_penetration(position, self.radius, other_position, other.radius)

    def check_collision_with_rect(self, other) -> Tuple[bool, Optional[Vector2], float]:
        position = self.owner.transform.position
        other_position = other.owner.transform.position
        return circle_rect_penetration(position, self.radius, other.width, other.height, other.x, other.y)

    def get_projection(self, axis='x'):
        if axis == "x":
            return self.owner.transform.position.x - self.radius, self.owner.transform.position.x + self.radius
        if axis == "y":
            return self.owner.transform.position.y - self.radius, self.owner.transform.position.y + self.radius


class RectCollider(Collider):
    def __init__(self, owner, width, height, group, mask, active=True, touchable=False):
        super().__init__(owner, group, mask, active, touchable)
        # центр прямоугольника = transform.position
        cx, cy = owner.transform.position.x, owner.transform.position.y
        self.x = cx - width / 2
        self.y = cy - height / 2
        self.width = width
        self.height = height

    def check_collision(self, other) -> Tuple[bool, Optional[Vector2], float]:
        if not self.active or not other.active:
            return False, None, 0
        if not self.can_collide_with(other):
            return False, None, 0
        return other.check_collision_with_rect(self)

    def check_collision_with_circle(self, circle):
        return circle.check_collision_with_rect(self)

    def check_collision_with_rect(self, other):
        normal, penetration = aabb_penetration(self.x, self.y, self.width, self.height,
                                               other.x, other.y, other.width, other.height)
        if penetration > 0:
            return True, normal, penetration
        else:
            return False, None, penetration

    def get_projection(self, axis='x'):
        if axis == "x":
            return self.owner.transform.position.x - self.width, self.owner.transform.position.x - self.width
        if axis == "y":
            return self.owner.transform.position.y - self.height, self.owner.transform.position.y - self.height
