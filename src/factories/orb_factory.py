import random

from src.registers.orb_registr import orb_register


class OrbFactory:
    @staticmethod
    def create_entity():
        record = random.choices(
            orb_register.records,
            weights=orb_register.weights,  # <- тут должно быть weights
            k=1
        )[0]
        orb = record.entity()
        return orb
