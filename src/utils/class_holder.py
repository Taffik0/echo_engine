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