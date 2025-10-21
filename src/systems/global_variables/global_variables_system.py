class GlobalVariablesSystem:
    variables = {}

    @classmethod
    def set_or_create(cls, name: str, data):
        """Создает или задает значение переменной"""
        cls.variables[name] = data

    @classmethod
    def get_variable(cls, name: str):
        """Возвращает переменную"""
        if name in cls.variables:
            return cls.variables[name]
        else:
            return None
