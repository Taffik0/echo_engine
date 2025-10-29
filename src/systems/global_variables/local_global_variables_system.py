from src.systems.event_system import EventSystem
from src.managers.save.save_manager import SaveManager

from src.systems.logger import Logger


class GlobalVariable:
    def __init__(self, data, is_saving):
        self.data = data
        self.is_saving = is_saving


class LocalGlobalVariablesSystem:
    def __init__(self, namespace):
        self.variables = {}
        self.namespace = namespace
        EventSystem.reg_event("end_game", self.save)
        EventSystem.reg_event("init", self.load)

    def set_or_create(self, name: str, data, is_saving=False):
        """Создает или задает значение переменной"""
        if name not in self.variables:
            variable = GlobalVariable(data, is_saving)
            self.variables[name] = variable
        else:
            self.variables[name].data = data

    def get_variable(self, name: str):
        """Возвращает переменную"""
        if name in self.variables:
            return self.variables[name].data
        else:
            return None

    def save(self):
        Logger.info("Saving variables...")
        save_data = {}
        for name, variable in self.variables.items():
            if variable.is_saving:
                save_data[name] = variable.data
        SaveManager.save("variables", "variables", save_data, namespace=self.namespace)

    def load(self):
        Logger.info("Load variables...")
        save_data = SaveManager.load("variables", "variables", namespace=self.namespace)
        for name, variable in save_data.items():
            self.variables[name] = GlobalVariable(variable, is_saving=True)



