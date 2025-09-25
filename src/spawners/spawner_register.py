import importlib
import pkgutil

spawners = []


def add_spawner(spawner):
    spawners.append(spawner)


def remove_all_spawners():
    global spawners
    spawners = []


def reset_spawners():
    for spawner in spawners:
        spawner.reset()


def spawners_update(dt):
    for spawner in spawners:
        spawner.update(dt)


