from enum import Enum, auto


class MenuAction(Enum):
    """Actions that can be returned from menu screens"""
    NEW_GAME = auto()
    LOAD_GAME = auto()
    SETTINGS = auto()
    EXIT = auto()
    RETURN_TO_MAIN = auto()
