from src.systems.event_system import EventSystem
from src.managers.sound_manager import SoundManager

from .worker_register import WorkerRegister
from .worker import Worker

from src.utils.class_holder import ClassHolder

from src.settings import START_MESSAGE


class StartWorker(Worker):
    def __init__(self):
        super().__init__()
        EventSystem.reg_event("start", self.start)

    @staticmethod
    def start():
        print(START_MESSAGE)

    def reset(self):
        pass


WorkerRegister.add_worker_prefab(ClassHolder(StartWorker))
