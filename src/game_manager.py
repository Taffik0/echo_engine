import inspect

from src.physics.collision_system import collision_manager
from src.physics.vectors import Vector2
from src.physics.transform import Transform


class GameManager:
    game = None

    @classmethod
    def destroy_me(cls, entity):
        collection = cls.game.entities
        if collection and entity in collection:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            collection.remove(entity)

    @classmethod
    def destroy_collider(cls, collider):
        collision_manager.unregister(collider)

    @classmethod
    def hard_remove(cls, entity, entity_type: str):
        if cls.game.entities and entity in cls.game.entities:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            cls.game.entities.remove(entity)

    @classmethod
    def hard_remove_list(cls, entity_list, entity_type: str):
        for entity in entity_list[:]:  # копия списка, чтобы безопасно удалять
            cls.hard_remove(entity, entity_type)

    @classmethod
    def spawn_entity(cls, entity, transform: Transform = None, position: Vector2 = None):
        if transform:
            entity.transform = transform
        elif position:
            entity.transform.position = position
        cls.game.entities.append(entity)
        entity.start()

    @classmethod
    def get_entity_by_tag(cls, tag):
        return [e for e in cls.game.entities if tag in e.tags]

    @classmethod
    def get_canvases(cls):
        return cls.game.canvases


class ComponentsManager:

    @classmethod
    def get_entities_with_components(cls, component_types: list):
        """
        Возвращает список всех сущностей, которые имеют все компоненты из component_types
        """
        result = []
        for entity in GameManager.game.entities:
            if all(comp_type in entity.components for comp_type in component_types):
                result.append(entity)
        return result
