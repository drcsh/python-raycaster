from enum import Enum, auto


class MainMenuAction(Enum):
    """Actions that can be returned from menu screens"""
    NEW_GAME = auto()
    LOAD_GAME = auto()
    SETTINGS = auto()
    EXIT = auto()
    SHOW_MAIN_MENU = auto()
