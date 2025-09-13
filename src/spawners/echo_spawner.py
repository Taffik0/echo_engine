from src.spawners.spawner import Spawner
from src.spawners import spawner_register

from src.game_manager import GameManager

from src.entities.echo import Echo, EchoSpawner

from src.settings import ECHO_SPAWN_DELAY, DIFF_ECHO_DELAY_MULT, DIFF_EVERY


class EchoSpawnerSpawner(Spawner):
    def spawn(self):
        player_x = GameManager.game.player.x
        player_y = GameManager.game.player.y
        echo = Echo(1, 1)
        spawner = EchoSpawner(2, entity=echo, entity_type="echo")
        GameManager.spawn_entity(spawner, "entity", player_x, player_y)


spawner_register.add_spawner(EchoSpawnerSpawner(ECHO_SPAWN_DELAY, DIFF_ECHO_DELAY_MULT, DIFF_EVERY, None))
