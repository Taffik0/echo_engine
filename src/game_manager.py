import inspect
from typing import TYPE_CHECKING

from src.physics.vectors import Vector2
from src.physics.transform import Transform

from src.render.canvas import Canvas

if TYPE_CHECKING:
    from src.core.scene.scene import Scene


class GameManager:
    game = None

    @classmethod
    def active_scene(cls) -> "Scene":
        return cls.game.active_scene

    @classmethod
    def set_active_scene(cls, scene: "Scene"):
        cls.game.active_scene = scene

    @classmethod
    def destroy_me(cls, entity):
        """Уничтожает сущность"""
        collection = cls.game.entities
        if collection and entity in collection:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            collection.remove(entity)

    @classmethod
    def destroy_collider(cls, collider):
        """Уничтожает коллайдер"""
        cls.active_scene().collision_system.unregister(collider)

    @classmethod
    def hard_remove(cls, entity):
        """Уничтожает сущность без вызова destroy"""
        if cls.game.entities and entity in cls.game.entities:
            if entity.collider:
                cls.destroy_collider(entity.collider)
            cls.game.entities.remove(entity)

    @classmethod
    def hard_remove_list(cls, entity_list):
        """Уничтожает список сущностей без вызова destroy"""
        for entity in entity_list[:]:  # копия списка, чтобы безопасно удалять
            cls.hard_remove(entity)

    @classmethod
    def spawn_entity(cls, entity, transform: Transform = None, position: Vector2 = None):
        """Спавнит сущность"""
        if transform:
            entity.transform = transform
        elif position:
            entity.transform.position = position
        cls.game.entities.append(entity)
        entity.start()

    @classmethod
    def get_entity_by_tag(cls, tag):
        """Возвращает список сущностей с определенным тегом"""
        return [e for e in cls.game.entities if tag in e.tags]

    @classmethod
    def get_canvases(cls) -> list[Canvas]:
        """Возвращает список канвасов"""
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
