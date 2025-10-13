import random
from src.settings import WIDTH, HEIGHT, ENEMY_SPAWN_EVERY, DIFF_EVERY, DIFF_ENEMY_RATE_MULT, DIFF_ENEMY_SPEED_ADD

from src.spawners.spawner import Spawner
from src.factories.enemy_factory import EnemyFactory

from src.game_manager import GameManager

from src.spawners import spawner_register

from src.physics.vectors import Vector2


class EnemySpawner(Spawner):
    def __init__(self, diff_enemy_speed_add, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diff_enemy_speed_add = diff_enemy_speed_add
        self.enemy_speed_boost = diff_enemy_speed_add
        self.start_enemy_speed_boost = diff_enemy_speed_add

    def spawn(self):
        enemy = self.factory.create_entity(self.enemy_speed_boost)
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x, y = random.uniform(0, WIDTH), -enemy.r - 4
        elif edge == 'bottom':
            x, y = random.uniform(0, WIDTH), HEIGHT + enemy.r + 4
        elif edge == 'left':
            x, y = -enemy.r - 4, random.uniform(0, HEIGHT)
        else:
            x, y = WIDTH + enemy.r + 4, random.uniform(0, HEIGHT)
        GameManager.spawn_entity(enemy, position=Vector2(x, y))

    def diff_add(self):
        super().diff_add()
        self.enemy_speed_boost += self.diff_enemy_speed_add

    def reset(self):
        super().reset()
        self.enemy_speed_boost = self.start_enemy_speed_boost


spawner_register.add_spawner(
    EnemySpawner(DIFF_ENEMY_SPEED_ADD,
                 ENEMY_SPAWN_EVERY,
                 DIFF_ENEMY_RATE_MULT,
                 DIFF_EVERY,
                 EnemyFactory())
)
print(spawner_register.spawners)
