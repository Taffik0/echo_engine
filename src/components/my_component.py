from src.components.component import Component


class MyComponent(Component):
    def start(self):
        print(self.owner.tags)
