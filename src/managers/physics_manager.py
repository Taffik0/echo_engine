from src.game_manager import GameManager


class PhysicsManager:
    @classmethod
    def register(cls, physics_body):
        physics_system = GameManager.active_scene().physics_system
        physics_system.physics_bodies.append(physics_body)

    @classmethod
    def unregister(cls, physics_body):
        physics_system = GameManager.active_scene().physics_system
        if physics_body in physics_system.physics_bodies:
            physics_system.physics_bodies.remove(physics_body)
    