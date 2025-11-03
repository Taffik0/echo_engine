class ClassHolder:
    def __init__(self, cls, *args, **kwargs):
        """
        cls — класс, который нужно хранить
        args, kwargs — параметры конструктора
        """
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def create_instance(self):
        """Создает экземпляр сохранённого класса"""
        return self.cls(*self.args, **self.kwargs)

    def __repr__(self):
        return f"<ClassHolder {self.cls.__name__} args={self.args} kwargs={self.kwargs}>"


class SceneHolder:
    def __init__(self, cls, name: str = None, workers:
                 list = None, spawners: list = None, entities: list = None, visual_effects: list = None):
        self.cls = cls
        self.name = name
        self.workers = workers
        self.spawners = spawners
        self.entities = entities
        self.visual_effects = visual_effects

    def create_instance(self):
        return self.cls(name=self.name, workers=self.workers, spawners=self.spawners, entities=self.entities,
                        visual_effects=self.visual_effects)
