from src.systems.event_system import EventSystem
from src.managers.sound_manager import SoundManager

from .worker_register import WorkerRegister
from .worker import Worker

from src.utils.class_holder import ClassHolder


class StartWorker(Worker):
    def __init__(self):
        super().__init__()
        EventSystem.reg_event("start", self.start)

    def start(self):
        print("game started")
        #SoundManager.load_and_run_sound(path="assets/music/untitled.wav", loops=-1)

    def reset(self):
        pass
        #SoundManager.load_and_run_sound(path="assets/music/untitled.wav", loops=-1)


WorkerRegister.add_worker_prefab(ClassHolder(StartWorker))
