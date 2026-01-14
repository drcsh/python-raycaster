import pygame_gui

from .player_hp_panel import PlayerHPPanel
from ...levelmanager import LevelManager


class HUD:
    """
    Data class for initialising the HUD and keeping track of the UI elements when in a level
    """

    def __init__(self, level_state: LevelManager, gui_manager: pygame_gui.UIManager):
        self.level_state = level_state
        self.player_hp_panel = PlayerHPPanel(gui_manager)

    def update(self):
        """
        Update UI elements based on the current level_state
        :param LevelManager level_state:
        :return:
        """

        self.player_hp_panel.update(f"{self.level_state.player.hp}")
