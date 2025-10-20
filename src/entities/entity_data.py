from pygame import Surface

from src.physics.transform import Transform

from src.systems.event_system import LocalEventSystem


class EntityData:

    def __init__(self, transform: Transform = None):
        self.tags = ["entity"]
        self.entity_name = ""
        self.collider = None
        self.color = (0, 0, 0)
        self.visible = True
        self.transform: Transform = transform if transform is not None else Transform()
        self.components = []
        self.event_system = LocalEventSystem()
        self.is_started = False

    def update(self, dt):
        """Вызывается при обновлении"""
        pass

    def draw(self, surf) -> Surface:
        """Вызывается при отрисовке"""
        pass

    def start(self):
        self.is_started = True
        for component in self.components:
            component.start()

    def destroy(self):
        """Метод уничтожения"""
        pass

    def on_collision(self, other):
        """Вызывается при столкновении"""
        pass

    def add_component(self, component):
        """Добавляет компонент (без ограничения по типу)."""
        self.components.append(component)
        component.owner = self
        if self.is_started:
            component.start()

    def has_component(self, comp_type):
        """Проверяет, есть ли хотя бы один компонент указанного типа."""
        return any(isinstance(c, comp_type) for c in self.components)

    def get_components(self, comp_type):
        """Возвращает список всех компонентов указанного типа."""
        return [c for c in self.components if isinstance(c, comp_type)]

    def get_component(self, comp_type):
        """Возвращает первый компонент указанного типа (для удобства)."""
        for c in self.components:
            if isinstance(c, comp_type):
                return c
        return None

    def remove_component(self, component):
        """Удаляет конкретный экземпляр компонента."""
        if component in self.components:
            self.components.remove(component)

    def remove_components_of_type(self, comp_type):
        """Удаляет все компоненты указанного типа."""
        self.components = [c for c in self.components if not isinstance(c, comp_type)]
