from src.utils.class_holder import ClassHolder

from src.settings import REPLACE_WORKER_PREFAB


class LocalWorkerRegister:
    def __init__(self):
        self.workers = []
        self.workers_prefabs: list[ClassHolder] = []

    def add_worker(self, worker):
        self.workers.append(worker)

    def add_worker_prefab(self, worker: ClassHolder):
        self.workers_prefabs.append(worker)

    def add_and_init_worker_prefab(self, worker: ClassHolder):
        self.workers_prefabs.append(worker)
        self.workers.append(worker.create_instance())

    def init_workers(self):
        for worker_prefab in self.workers_prefabs:
            self.workers.append(worker_prefab.create_instance())

    def remove_all_workers(self):
        self.workers = []

    def reset_workers(self):
        if REPLACE_WORKER_PREFAB:
            self.remove_all_workers()
            self.init_workers()
        else:
            for worker in self.workers:
                worker.reset()

    def workers_update(self, dt):
        for worker in self.workers:
            worker.update(dt)
