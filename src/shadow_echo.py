

from src.game import Game
from src.game_manager import GameManager
import src.physics.colision_manager

from src.spawners import spawner_register
from src.workers import worker_register
import src.visual_effects

# ------------------------------
# SHADOW ECHO — Endless Mini-Arcade
# ------------------------------
# Unique twist: your past positions spawn deadly "echoes" that clutter the arena.
# Grab green Sync Orbs to absorb ALL echoes into score and clear the field.
# Difficulty ramps up over time: more/faster enemies, more frequent echoes.
# Controls: WASD / Arrow Keys to move, SPACE to dash, SHIFT to slow-time (costs focus), R to restart, ESC to quit.
# 
# Tested with pygame 2.x



if __name__ == "__main__":
    game = Game()
    GameManager.game = game
    game.reset()  # init вызывается внутри reset
    game.start()
    game.run()
