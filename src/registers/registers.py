from src.entities.enemy import Enemy, FastEnemy


class RegisterRecord:
    entity = None
    name = None

    def __init__(self, entity, name):
        self.entity = entity
        self.name = name


class Register:
    def __init__(self):
        self.records = []
        self.weights = []

    def add_record(self, record: RegisterRecord, weight):
        self.records.append(record)
        self.weights.append(weight)

    def add_record_list(self, record_list):
        for record in record_list:
            self.add_record(record[0], record[1])



