import time
import atexit
import signal
import sys
from io import TextIOWrapper
from pathlib import Path

from src.settings import DEBUG


# ANSI коды для текста
ANSI_TEXT_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",  # сброс всех стилей
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m"
}

# ANSI коды для фона
ANSI_BG_COLORS = {
    "black": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
    "bright_black": "\033[100m",
    "bright_red": "\033[101m",
    "bright_green": "\033[102m",
    "bright_yellow": "\033[103m",
    "bright_blue": "\033[104m",
    "bright_magenta": "\033[105m",
    "bright_cyan": "\033[106m",
    "bright_white": "\033[107m"
}


class Logger:
    logs_file = None

    @classmethod
    def init(cls, INFO_LOGS_DIR):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        file_path = Path(f"{INFO_LOGS_DIR}/log_{now_time}.txt")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
        cls.logs_file = open(file_path, "a")
        atexit.register(cls.close)  # Автоматически закрывает файл при завершении

    @classmethod
    def close(cls):
        cls.logs_file.close()

    @classmethod
    def _write_into_log_file(cls, text):
        cls.logs_file.write(f"{text}\n")

    @classmethod
    def print(cls, text: str):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        message = f"[{now_time}] {text}"
        print(message)
        cls._write_into_log_file(message)

    @classmethod
    def info(cls, text: str):
        message = f"{ANSI_TEXT_COLORS["green"]}INFO {ANSI_TEXT_COLORS["reset"]} {text}"
        cls.print(message)

    @classmethod
    def warning(cls, text: str):
        message = f"{ANSI_TEXT_COLORS["yellow"]}WARNING {ANSI_TEXT_COLORS["reset"]} {text}"
        cls.print(message)

    @classmethod
    def error(cls, text: str):
        message = f"{ANSI_TEXT_COLORS["red"]}ERROR {text} {ANSI_TEXT_COLORS["reset"]}"
        cls.print(message)

    @classmethod
    def debug(cls, text: str):
        if DEBUG:
            message = f"{ANSI_TEXT_COLORS["blue"]}DEBUG {text} {ANSI_TEXT_COLORS["reset"]}"
            cls.print(message)
