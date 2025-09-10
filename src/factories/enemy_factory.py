import random

from src.settings import *

from src.registers import enemy_register
from src.game_manager import GameManager


class EnemyFactory:
    @staticmethod
    def create_enemy(speed_boost):
        record = random.choices(
            enemy_register.enemies,
            weights=enemy_register.weight,  # <- тут должно быть weights
            k=1
        )[0]
        enemy = record.entity(speed_boost)
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            enemy.x, enemy.y = random.uniform(0, WIDTH), -enemy.r - 4
        elif edge == 'bottom':
            enemy.x, enemy.y = random.uniform(0, WIDTH), HEIGHT + enemy.r + 4
        elif edge == 'left':
            enemy.x, enemy.y = -enemy.r - 4, random.uniform(0, HEIGHT)
        else:
            enemy.x, enemy.y = WIDTH + enemy.r + 4, random.uniform(0, HEIGHT)
        GameManager.game.enemies.append(enemy)
        enemy.start()
