import random

from src.settings import WIDTH, HEIGHT, ORB_SPAWN_EVERY, DIFF_ORB_RATE_MULT, DIFF_EVERY
from src.game_manager import GameManager

from src.spawners.spawner import Spawner
from src.spawners import spawner_register

from src.factories.orb_factory import OrbFactory


class OrbSpawner(Spawner):
    def spawn(self):
        margin = 30
        x = random.uniform(margin, WIDTH - margin)
        y = random.uniform(margin, HEIGHT - margin)
        orb = self.factory.create_entity()
        GameManager.spawn_entity(orb, "orb", x, y)


spawner_register.add_spawner(OrbSpawner(ORB_SPAWN_EVERY, DIFF_ORB_RATE_MULT, DIFF_EVERY, OrbFactory))