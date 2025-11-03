from src.core.game import Game
from src.game_manager import GameManager
from src.systems.logger import Logger
from src.systems.crash_handler import CrashHandler
import src.path as path

# ------------------------------
# ECHO ENGINE — Mini game engine on python
# ------------------------------
# Tested with pygame 2.x


if __name__ == "__main__":
    Logger.init(path.INFO_LOGS_DIR)
    CrashHandler.init(path.CRASH_LOGS_DIR)
    path.print_status()
    game = Game()
    Logger.info("Game inited")
    GameManager.game = game
    game.start()
    Logger.close()
