import importlib
import pkgutil


class SpawnersRegister:
    def __init__(self):
        self.spawners = []

    def add_spawner(self, spawner):
        self.spawners.append(spawner)

    def remove_all_spawners(self):
        self.spawners = []

    def reset_spawners(self):
        for spawner in self.spawners:
            spawner.reset()

    def spawners_update(self, dt):
        for spawner in self.spawners:
            spawner.update(dt)


