from src.game_manager import GameManager
from src.core.scene.scene import Scene
from src.utils.class_holder import SceneHolder


class SceneManager:

    # === Смена сцен ===
    @classmethod
    def switch(cls, name: str) -> None:
        """Меняет активную сцену, не выгружая предыдущую (пауза/переключение)."""
        scenes_prefab: list[SceneHolder] = GameManager.game.scenes_prefab
        scenes_loaded: list[Scene] = GameManager.game.scenes_loaded

        scenes_loaded_dict = {scene.name: scene for scene in scenes_loaded}
        scenes_prefab_dict = {scene.name: scene for scene in scenes_prefab}

        if name in scenes_loaded_dict:
            GameManager.set_active_scene(scenes_loaded_dict[name])
        elif name in scenes_prefab_dict:
            scene = scenes_prefab_dict[name].create_instance()
            GameManager.game.scenes_loaded.append(scene)
            GameManager.active_scene().unload()
            GameManager.set_active_scene(scene)

    @classmethod
    def change(cls, name: str) -> None:
        """Меняет сцену и выгружает предыдущую (полная замена)."""
        scenes_prefab: list[SceneHolder] = GameManager.game.scenes_prefab
        scenes_loaded: list[Scene] = GameManager.game.scenes_loaded

        scenes_loaded_dict = {scene.name: scene for scene in scenes_loaded}
        scenes_prefab_dict = {scene.name: scene for scene in scenes_prefab}

        GameManager.game.scenes_loaded.remove(GameManager.active_scene())
        scene = GameManager.active_scene()
        if name in scenes_loaded_dict:
            cls.unload(scene.name)

            GameManager.set_active_scene(scenes_loaded_dict[name])
        elif name in scenes_prefab_dict:
            cls.unload(scene.name)
            cls.load(name)

    # === Загрузка / выгрузка ===
    @classmethod
    def load(cls, name: str):
        scenes_prefab: list[SceneHolder] = GameManager.game.scenes_prefab
        scenes_loaded: list[Scene] = GameManager.game.scenes_loaded
        scenes_loaded_dict = {scene.name: scene for scene in scenes_loaded}
        scenes_prefab_dict = {scene.name: scene for scene in scenes_prefab}
        if name in scenes_prefab_dict and name not in scenes_loaded_dict:
            scene: Scene = scenes_prefab_dict[name].create_instance()
            GameManager.game.scenes_loaded.append(scene)
            scene.event_system.trigger_event("start")

    @classmethod
    def unload(cls, name: str) -> None:
        scenes_prefab: list[SceneHolder] = GameManager.game.scenes_prefab
        scenes_loaded: list[Scene] = GameManager.game.scenes_loaded
        scenes_loaded_dict = {scene.name: scene for scene in scenes_loaded}
        scenes_prefab_dict = {scene.name: scene for scene in scenes_prefab}
        if name in scenes_prefab_dict and name in scenes_loaded_dict:
            scene: Scene = scenes_loaded_dict[name]
            GameManager.game.scenes_loaded.remove()
            scene.event_system.trigger_event("game_end")

    # === Утилиты ===
    @classmethod
    def get(cls, name: str) -> Scene | None:
        """Возвращает сцену по имени (если загружена)."""

    @classmethod
    def reload(cls, name: str) -> None:
        """Полностью перезагружает сцену."""
