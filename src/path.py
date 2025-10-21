import os


current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# Корень проекта
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Папка для сохранений
SAVES_DIR = os.path.join(PROJECT_ROOT, "saves")
os.makedirs(SAVES_DIR, exist_ok=True)

# Папка с ресурсами
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

print(PROJECT_ROOT)
print(SAVES_DIR)
print(ASSETS_DIR)
