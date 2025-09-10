from src.entities.enemy import Enemy, FastEnemy


class RegisterRecord:
    entity = None
    name = None

    def __init__(self, entity, name):
        self.entity = entity
        self.name = name


class EnemyRegister:
    enemies = []
    weight = []

    def add_enemy(self, enemy: RegisterRecord, weight):
        self.enemies.append(enemy)
        self.weight.append(weight)

    def add_enemy_list(self, enemies_list):
        for enemy in enemies_list:
            self.add_enemy(enemy[0], enemy[1])


enemies_list = [(RegisterRecord(Enemy, "Enemy"), 90),
                (RegisterRecord(FastEnemy, "FastEnemy"), 10)]
enemy_register = EnemyRegister()
enemy_register.add_enemy_list(enemies_list)
