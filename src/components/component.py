from src.entities.entity_data import EntityData


class Component:
    def __init__(self, owner: EntityData | None = None):
        self.owner: EntityData | None = owner
          
    def start(self):
        pass

    def update(self):
        pass
