class Collider:
    def __init__(self, owner, radius, group, mask, active=True):
        self.owner = owner
        self.radius = radius
        self.group = group      # слой (например "enemy")
        self.mask = mask        # список слоёв, с которыми взаимодействует
        self.active = active

    def can_collide_with(self, other):
        return other.group in self.mask and self.group in other.mask

    def check_collision(self, other):
        if not self.active or not other.active:
            return False
        if not self.can_collide_with(other):
            return False
        dx = self.owner.x - other.owner.x
        dy = self.owner.y - other.owner.y
        return dx*dx + dy*dy <= (self.radius + other.radius)**2