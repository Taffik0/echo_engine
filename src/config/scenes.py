from src.utils.class_holder import SceneHolder
from src.core.scene.scene import Scene

from src.workers.dev.start_worker import StartWorker


SCENES: list[SceneHolder] = [
    SceneHolder(Scene, name="main")
]
