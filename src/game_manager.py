class GameManager:
    game = None

    player = None
    enemies = []
    orbs = []
    echoes = []

    @classmethod
    def destroy_me(cls, entity, entity_type: str):
        if entity_type == "enemy":
            cls.game.enemies.remove(entity)
        if entity_type == "orbs":
            cls.game.orbs.remove(entity)
        if entity_type == "echoes":
            cls.game.echoes.remove(entity)

    @classmethod
    def init(cls):
        cls.player = cls.game.player
        cls.enemies = cls.game.enemies
        cls.orbs = cls.game.orbs
        cls.echoes = cls.game.echoes

