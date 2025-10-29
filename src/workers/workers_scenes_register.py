from src.utils.class_holder import ClassHolder
from .dev.start_worker import StartWorker


class WorkerSceneRecord:
    def __init__(self, worker_prefab, scene_name):
        self.worker_prefab = worker_prefab
        self.scene_name = scene_name


WORKERS_SCENES_REGISTER: list[WorkerSceneRecord] = []
