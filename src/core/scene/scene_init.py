from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.utils.class_holder import SceneHolder

from src.config.scenes import SCENES
from src.workers.workers_scenes_register import WorkerSceneRecord, WORKERS_SCENES_REGISTER


def scenes_init():
    scenes = []
    for scene_holder in SCENES:
        scenes.append(scene_holder)
    return scenes


# scenes - {name: scene}
def worker_scenes_init(scenes: dict[str, "SceneHolder"]):
    for worker_record in WORKERS_SCENES_REGISTER:
        scene_name = worker_record.scene_name
        if scene_name in scenes:
            scenes[scene_name].workers.append(worker_record.worker_prefab)

