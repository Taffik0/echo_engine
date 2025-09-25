class Collider:
    def __init__(self, owner, group, mask, active=True):
        self.owner = owner
        self.group = group
        self.mask = mask
        self.active = active

    def can_collide_with(self, other):
        return other.group in self.mask and self.group in other.mask

    def check_collision(self, other):
        raise NotImplementedError


class CircleCollider(Collider):
    def __init__(self, owner, radius, group, mask, active=True):
        super().__init__(owner, group, mask, active)
        self.radius = radius

    def check_collision(self, other):
        if not self.active or not other.active:
            return False
        if not self.can_collide_with(other):
            return False
        return other.check_collision_with_circle(self)

    def check_collision_with_circle(self, other):
        dx = self.owner.position.x - other.owner.position.x
        dy = self.owner.position.y - other.owner.position.y
        return dx*dx + dy*dy <= (self.radius + other.radius)**2

    def check_collision_with_rect(self, rect):
        cx, cy = self.owner.position.x, self.owner.position.y
        # ближайшая точка на прямоугольнике
        nearest_x = max(rect.x, min(cx, rect.x + rect.width))
        nearest_y = max(rect.y, min(cy, rect.y + rect.height))
        dx = cx - nearest_x
        dy = cy - nearest_y
        return dx*dx + dy*dy <= self.radius * self.radius


class RectCollider(Collider):
    def __init__(self, owner, width, height, group, mask, active=True):
        super().__init__(owner, group, mask, active)
        self.x = owner.position.x - width / 2
        self.y = owner.position.y - height / 2
        self.width = width
        self.height = height

    def check_collision(self, other):
        if not self.active or not other.active:
            return False
        if not self.can_collide_with(other):
            return False
        return other.check_collision_with_rect(self)

    def check_collision_with_circle(self, circle):
        return circle.check_collision_with_rect(self)

    def check_collision_with_rect(self, other):
        return not (self.x + self.width < other.x or
                    self.x > other.x + other.width or
                    self.y + self.height < other.y or
                    self.y > other.y + other.height)
