# To prevent circular imports, this file should import as little as possible.


class GameState:
    """
    Keeps references objects important for the state of the game.

    Todo: provide save and load functionality!
    """

    def __init__(self, player, level):

        self.player = player
        self.level = level
