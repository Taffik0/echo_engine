from src.utils.class_holder import ClassHolder
from src.core.scene.scene import Scene

from src.workers.start_worker import StartWorker

SCENES: list[ClassHolder] = [
    ClassHolder(Scene, name="main")
]
