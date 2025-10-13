from pygame import Surface

from src.physics.transform import Transform


class EntityData:

    def __init__(self, transform: Transform = None):
        self.tags = ["entity"]
        self.entity_name = ""
        self.collider = None
        self.color = (0, 0, 0)
        self.visible = True
        self.transform: Transform = transform if transform is not None else Transform()
        self.components = {}

    def update(self, dt):
        pass

    def draw(self, surf) -> Surface:
        pass

    def start(self):
        pass

    def destroy(self):
        pass

    def on_collision(self, other):
        pass

    def add_component(self, component):
        self.components[type(component)] = component

    def has_component(self, comp_type):
        return comp_type in self.components

    def get_component(self, comp_type):
        return self.components.get(comp_type, None)
