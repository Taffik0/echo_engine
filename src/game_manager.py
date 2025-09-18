from src.physics.colision_manager import collision_manager


class GameManager:
    game = None

    @classmethod
    def destroy_me(cls, entity, entity_type: str):
        collections = {
            "enemy": cls.game.entities,
            "orb": cls.game.entities,
            "echo": cls.game.entities,
            "entity": cls.game.entities
        }

        collection = collections.get(entity_type)
        if collection and entity in collection:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            collection.remove(entity)


    @classmethod
    def destroy_collider(cls, collider):
        collision_manager.unregister(collider)

    @classmethod
    def hard_remove(cls, entity, entity_type: str):
        collections = {
            "enemy": cls.game.entities,
            "orb": cls.game.entities,
            "echo": cls.game.entities,
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
            "enemy": cls.game.entities,
            "orb": cls.game.entities,
            "echo": cls.game.entities,
            "entity": cls.game.entities
        }
        entity.x = x
        entity.y = y
        collection = collections.get(entity_type)
        collection.append(entity)
        entity.start()

    @classmethod
    def get_entity_by_tag(cls, tag):
        return [e for e in cls.game.entities if tag in e.tags]
