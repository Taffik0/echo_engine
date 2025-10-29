from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.scene.scene import Scene

from src.config.scenes import SCENES
from src.workers.workers_scenes_register import WorkerSceneRecord, WORKERS_SCENES_REGISTER


def scenes_init():
    scenes = []
    for scene_holder in SCENES:
        scenes.append(scene_holder.create_instance())
    return scenes


# scenes - {name: scene}
def worker_scenes_init(scenes: dict[str, "Scene"]):
    for worker_record in WORKERS_SCENES_REGISTER:
        scene_name = worker_record.scene_name
        if scene_name in scenes:
            scenes[scene_name].worker_register.add_and_init_worker_prefab(worker_record.worker_prefab)
