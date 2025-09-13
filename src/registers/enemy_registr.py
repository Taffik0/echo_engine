from src.registers.registers import Register, RegisterRecord

from src.entities.enemy import Enemy, FastEnemy

class EnemyRegister(Register):
    pass


enemies_list = [(RegisterRecord(Enemy, "Enemy"), 90),
                (RegisterRecord(FastEnemy, "FastEnemy"), 10)]
enemy_register = EnemyRegister()
enemy_register.add_record_list(enemies_list)
