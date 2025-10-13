from src.spawners.spawner import Spawner
from src.spawners import spawner_register

from src.game_manager import GameManager

from src.entities.echo import Echo, EchoSpawner

from src.settings import ECHO_SPAWN_DELAY, DIFF_ECHO_DELAY_MULT, DIFF_EVERY

from src.physics.vectors import Vector2


class EchoSpawnerSpawner(Spawner):
    def spawn(self):
        player_x = GameManager.game.player.transform.position.x
        player_y = GameManager.game.player.transform.position.y
        echo = Echo
        spawner = EchoSpawner(2, entity=echo, entity_type="echo")
        GameManager.spawn_entity(spawner, position=Vector2(player_x, player_y))


spawner_register.add_spawner(EchoSpawnerSpawner(ECHO_SPAWN_DELAY, DIFF_ECHO_DELAY_MULT, DIFF_EVERY, None))
