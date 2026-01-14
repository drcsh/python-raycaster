
class GameExitException(BaseException):
    """
    Thrown to exit the game
    """
    pass


class PlayerDeadException(BaseException):
    """
    Thrown when the player dies.
    """
    pass


class LevelCompleteException(BaseException):
    """
    Thrown when all enemies in a level are defeated.
    """
    pass
