from src.systems.global_variables.global_variables_system import GlobalVariablesSystem
from src.game_manager import GameManager


class GlobalVariableManager:
    @classmethod
    def set_or_create(cls, name: str, data, is_saving=False, is_global = False):
        if is_global:
            GlobalVariablesSystem.set_or_create(name, data, is_saving)
        else:
            GameManager.active_scene().global_variable_system.set_or_create(name, data, is_saving)

    @classmethod
    def get_variable(cls, name: str, is_global):
        if is_global:
            return GlobalVariablesSystem.get_variable(name)
        else:
            return GameManager.active_scene().global_variable_system.get_variable(name)