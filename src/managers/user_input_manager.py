from src.systems.user_imput.user_input_system import UserInputSystem, InputKey, KeyEvent
from src.game_manager import GameManager


class UserInputManager:
    @classmethod
    def registration_event(cls, key_event: KeyEvent, is_global=False):
        if is_global:
            UserInputSystem.registration_event(key_event)
        else:
            GameManager.active_scene().user_input_system.registration_event(key_event)

    @classmethod
    def unregister_event(cls, key_event: KeyEvent, is_global=False):
        if is_global:
            UserInputSystem.unregister_event(key_event)
        else:
            GameManager.active_scene().user_input_system.unregister_event(key_event)

    @classmethod
    def get_key(cls, key, is_global=False):
        if is_global:
            return UserInputSystem.get_key(key)
        else:
            return GameManager.active_scene().user_input_system.get_key(key)
