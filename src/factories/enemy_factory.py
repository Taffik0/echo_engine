import random

from src.settings import *

from src.registers.enemy_registr import enemy_register
from src.game_manager import GameManager


class EnemyFactory:
    @staticmethod
    def create_entity(speed_boost):
        # выбрать один RegisterRecord по весам
        record = random.choices(
            enemy_register.records,
            weights=enemy_register.weights,
            k=1
        )[0]
        # создать объект
        enemy = record.entity(speed_boost)
        return enemy
