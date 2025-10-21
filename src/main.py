import src.path

from src.game import Game
from src.game_manager import GameManager
import src.physics.collision_system

from src.spawners import spawner_register
from src.workers import worker_register
import src.visual_effects

# ------------------------------
# ECHO ENGINE — Mini game engine on python
# ------------------------------
# Tested with pygame 2.x



if __name__ == "__main__":
    game = Game()
    GameManager.game = game
    game.reset()  # init вызывается внутри reset
    game.start()
    game.run()
