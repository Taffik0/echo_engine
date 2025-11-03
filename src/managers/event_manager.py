from src.game_manager import GameManager
from src.systems.event_system import EventSystem


class EventManager:
    @classmethod
    def reg_event(cls, event_name, method, is_global=False):
        if is_global:
            EventManager.reg_event(event_name, method)
        else:
            GameManager.active_scene().event_system.reg_event(event_name, method)

    @classmethod
    def unregister_event(cls, event_name, method, is_global=False):
        if is_global:
            EventManager.unregister_event(event_name, method)
        else:
            GameManager.active_scene().event_system.unregister_event(event_name, method)

    @classmethod
    def trigger_event(cls, event_name, is_global=False, *args, **kwargs):
        if is_global:
            EventManager.trigger_event(event_name, *args, **kwargs)
        else:
            GameManager.active_scene().event_system.trigger_event(event_name, *args, **kwargs)