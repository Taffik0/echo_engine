from src.config.scenes import SCENES


def scenes_init():
    scenes = []
    for scene_holder in SCENES:
        scenes.append(scene_holder.create_instance())
    return scenes
