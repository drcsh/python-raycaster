from .player_hp_panel import PlayerHPPanel


class HUD:
    """
    Data class for initialising the HUD and keeping track of the UI elements when in a level
    """

    def __init__(self, gui_manager):

        self.player_hp_panel = PlayerHPPanel(gui_manager)

    def update(self, gamestate):
        """
        Update UI elements based on the current gamestate
        :param GameState gamestate:
        :return:
        """

        self.player_hp_panel.update(f"{gamestate.player.hp}")