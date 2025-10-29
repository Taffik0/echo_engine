# src/core/crash_handler.py
import os
import sys
import traceback
import datetime
import json

from .logger import Logger


class CrashHandler:
    REPORTS_DIR = "saves/crash_reports"

    @classmethod
    def init(cls, crash_report_dir):
        """Устанавливает глобальный перехватчик исключений."""
        cls.REPORTS_DIR = crash_report_dir
        sys.excepthook = cls.handle_exception
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)

    @classmethod
    def handle_exception(cls, exctype, value, tb):
        """Вызывается при любой необработанной ошибке."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(cls.REPORTS_DIR, f"crash_{timestamp}.json")

        report = {
            "timestamp": timestamp,
            "type": str(exctype.__name__),
            "message": str(value),
            "traceback": "".join(traceback.format_exception(exctype, value, tb)),
        }

        # Попробуем сохранить состояние игры, если возможно
        from src.game_manager import GameManager
        game = getattr(GameManager, "game", None)
        if game:
            report["game_state"] = cls.collect_game_state(game)

        with open(filename, "a", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=4)

        Logger.error("-==-==-==-==-==- GAME CRASHED! -==-==-==-==-==-")
        Logger.error(f"CRASH REPORT SAVED: {filename}\n")
        Logger.error(report["traceback"])
        sys.exit(1)

    @classmethod
    def collect_game_state(cls, game):
        """Собирает минимум полезных данных о состоянии движка."""
        try:
            return {
                "active_scene": getattr(game.active_scene, "name", None),
                "entities_count": len(getattr(game.active_scene, "entities", [])),
                "entities": getattr(game.active_scene, "entities", []),
                "workers_count": len(getattr(game.active_scene.worker_register, "workers", [])),
            }
        except Exception as e:
            return {"error_collecting_state": str(e)}