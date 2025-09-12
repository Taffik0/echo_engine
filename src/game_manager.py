from src.physics.colision_manager import collision_manager


class GameManager:
    game = None

    player = None
    enemies = []
    orbs = []
    echoes = []

    @classmethod
    def destroy_me(cls, entity, entity_type: str):
        collections = {
            "enemy": cls.game.enemies,
            "orb": cls.game.orbs,
            "echo": cls.game.echoes,
            "entity": cls.game.entities
        }

        collection = collections.get(entity_type)
        if collection and entity in collection:
            if entity.collider:
                cls.destroy_collider(entity.collider)
                if entity_type == "orb":
                    print(f"удалил орб с колайлором {entity}")
            collection.remove(entity)

    @classmethod
    def init(cls):
        cls.player = cls.game.player
        cls.enemies = cls.game.enemies
        cls.orbs = cls.game.orbs
        cls.echoes = cls.game.echoes

    @classmethod
    def destroy_collider(cls, collider):
        collision_manager.unregister(collider)

    @classmethod
    def hard_remove(cls, entity, entity_type: str):
        collections = {
            "enemy": cls.game.enemies,
            "orb": cls.game.orbs,
            "echo": cls.game.echoes,
            "entity": cls.game.entities
        }

        collection = collections.get(entity_type)
        if collection and entity in collection:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            collection.remove(entity)

    @classmethod
    def hard_remove_list(cls, entity_list, entity_type: str):
        for entity in entity_list[:]:  # копия списка, чтобы безопасно удалять
            cls.hard_remove(entity, entity_type)

    @classmethod
    def spawn_entity(cls, entity, entity_type, x, y):
        collections = {
            "enemy": cls.game.enemies,
            "orb": cls.game.orbs,
            "echo": cls.game.echoes,
            "entity": cls.game.entities
        }
        entity.x = x
        entity.y = y
        collection = collections.get(entity_type)
        collection.append(entity)


