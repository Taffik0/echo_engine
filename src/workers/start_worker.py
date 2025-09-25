from src.event_system import EventSystem

from .worker_register import add_worker
from .worker import Worker


class StartWarker(Worker):
    def __init__(self):
        super().__init__()
        EventSystem.reg_event("start", self.start)

    def start(self):
        print("game started")


worker = StartWarker()
add_worker(worker)
