from src.core.game import Game
from src.game_manager import GameManager

# ------------------------------
# ECHO ENGINE — Mini game engine on python
# ------------------------------
# Tested with pygame 2.x



if __name__ == "__main__":
    game = Game()
    GameManager.game = game
    #game.reset()  # init вызывается внутри reset
    game.start()
