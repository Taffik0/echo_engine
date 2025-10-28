import os
import json
from pathlib import Path

from src.path import SAVES_DIR

from src.systems.event_system import EventSystem


class SaveManager:
    @classmethod
    def save(cls, directory: str, file_name: str, data, namespace: str = "global"):
        file_path = Path(f"{SAVES_DIR}/{namespace}/{directory}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, directory: str, file_name: str, namespace: str = "global"):
        file_path = Path(f"{SAVES_DIR}/{namespace}/{directory}/{file_name}.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        if not file_path.exists():
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data_loaded = json.load(f)
            except json.JSONDecodeError:
                return {}
            return data_loaded
