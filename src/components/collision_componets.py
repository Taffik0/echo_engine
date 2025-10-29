from .component import Component

from src.physics.colliders import CircleCollider, RectCollider
from src.managers.collision_manager import CollisionManager


class CircleCollisionComponent(Component):
    def __init__(self, radius, group, mask, active=True, touchable=False, *args, **kwargs):
        super().__init__(**kwargs)
        self.circle_collider = CircleCollider(self.owner, radius, group, mask, active=active, touchable=touchable)

    def start(self):
        self.circle_collider.owner = self.owner
        CollisionManager.register(self.circle_collider)

    def on_delete(self):
        CollisionManager.unregister(self.circle_collider)


