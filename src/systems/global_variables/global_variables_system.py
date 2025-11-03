from src.systems.event_system import EventSystem
from src.managers.save.save_manager import SaveManager

from src.systems.logger import Logger


class GlobalVariable:
    def __init__(self, data, is_saving):
        self.data = data
        self.is_saving = is_saving


class GlobalVariablesSystem:
    variables = {}

    @classmethod
    def set_or_create(cls, name: str, data, is_saving=False):
        """Создает или задает значение переменной"""
        if name not in cls.variables:
            variable = GlobalVariable(data, is_saving)
            cls.variables[name] = variable
        else:
            cls.variables[name].data = data

    @classmethod
    def get_variable(cls, name: str):
        """Возвращает переменную"""
        if name in cls.variables:
            return cls.variables[name].data
        else:
            return None

    @classmethod
    def save(cls):
        Logger.info("Saving variables...")
        save_data = {}
        for name, variable in cls.variables.items():
            if variable.is_saving:
                save_data[name] = variable.data
        SaveManager.save("variables", "variables", save_data)

    @classmethod
    def load(cls):
        Logger.info("Load variables...")
        save_data = SaveManager.load("variables", "variables")
        for name, variable in save_data.items():
            cls.variables[name] = GlobalVariable(variable, is_saving=True)


EventSystem.reg_event("end_game", GlobalVariablesSystem.save)
EventSystem.reg_event("init", GlobalVariablesSystem.load)
