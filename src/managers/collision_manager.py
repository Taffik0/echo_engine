from src.game_manager import GameManager


class CollisionManager:
    @classmethod
    def register(cls, collider):
        active_scene = GameManager.active_scene()
        active_scene.collision_system.register(collider)

    @classmethod
    def unregister(cls, collider):
        collision_system = GameManager.active_scene().collision_system
        if collider in collision_system.colliders:
            collision_system.colliders.remove(collider)
