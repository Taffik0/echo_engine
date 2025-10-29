import importlib
import pkgutil
import os

# Импорт регистра воркеров
from . import worker_register

base_path = os.path.dirname(__file__)
dev_path = os.path.join(base_path, "dev")

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if module_name in ("worker_register", "__init__", "local_worker_register"):
        continue
    importlib.import_module(f"{__name__}.{module_name}")

if os.path.isdir(dev_path):
    for loader, module_name, is_pkg in pkgutil.iter_modules([dev_path]):
        importlib.import_module(f"{__name__}.dev.{module_name}")