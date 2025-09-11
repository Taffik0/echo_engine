from src.physics.colision_manager import collision_manager


class GameManager:
    game = None

    player = None
    enemies = []
    orbs = []
    echoes = []

    @classmethod
    def destroy_me(cls, entity, entity_type: str):
        if entity_type == "enemy":
            cls.destroy_collider(entity.collider)
            cls.game.enemies.remove(entity)
        if entity_type == "orb" and entity in cls.game.orbs:
            cls.destroy_collider(entity.collider)
            cls.game.orbs.remove(entity)
        if entity_type == "echo":
            cls.destroy_collider(entity.collider)
            cls.game.echoes.remove(entity)

    @classmethod
    def init(cls):
        cls.player = cls.game.player
        cls.enemies = cls.game.enemies
        cls.orbs = cls.game.orbs
        cls.echoes = cls.game.echoes

    @classmethod
    def destroy_collider(cls, collider):
        collision_manager.unregister(collider)

