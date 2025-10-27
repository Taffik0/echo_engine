from src.utils.class_holder import ClassHolder

from src.settings import REPLACE_WORKER_PREFAB


class WorkerRegister:
    workers = []
    workers_prefabs: list[ClassHolder] = []

    @classmethod
    def add_worker(cls, worker):
        cls.workers.append(worker)

    @classmethod
    def add_worker_prefab(cls, worker: ClassHolder):
        cls.workers_prefabs.append(worker)

    @classmethod
    def init_workers(cls):
        for worker_prefab in cls.workers_prefabs:
            cls.workers.append(worker_prefab.create_instance())

    @classmethod
    def remove_all_workers(cls):
        cls.workers = []

    @classmethod
    def reset_workers(cls):
        if REPLACE_WORKER_PREFAB:
            cls.remove_all_workers()
            cls.init_workers()
        else:
            for worker in cls.workers:
                worker.reset()

    @classmethod
    def workers_update(cls, dt):
        for worker in cls.workers:
            worker.update(dt)
