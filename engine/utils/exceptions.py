
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
