import os
from src.systems.logger import Logger


current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# Корень проекта
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Папка для сохранений
SAVES_DIR = os.path.join(PROJECT_ROOT, "saves")
os.makedirs(SAVES_DIR, exist_ok=True)

# Папка с ресурсами
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

# Папка с логами
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

INFO_LOGS_DIR = os.path.join(LOGS_DIR, "info")
CRASH_LOGS_DIR = os.path.join(LOGS_DIR, "crash")


def print_status():
    Logger.info(f"project root {PROJECT_ROOT} - found")
    Logger.info(f"saves dir {SAVES_DIR} - found")
    Logger.info(f"assets dir {ASSETS_DIR} - found")
    Logger.info(f"logs dir {LOGS_DIR} - found")
    Logger.info(f"logs dir info {INFO_LOGS_DIR} - found")
    Logger.info(f"logs dir crash {CRASH_LOGS_DIR} - found")


