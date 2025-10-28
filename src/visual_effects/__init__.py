import importlib
import pkgutil

# сначала явно импортируем регистр
from . import visual_effects_register

# потом все остальные модули в папке spawners (кроме spawner_register и __init__)
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if module_name in ("visual_effects_registr", "__init__"):
        continue
    importlib.import_module(f"{__name__}.{module_name}")