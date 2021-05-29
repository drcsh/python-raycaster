import pygame
import pygame_gui


class PlayerHPPanel:
    """
    UI Element for displaying the player's HP. Appears in the bottom left of the screen.
    """

    def __init__(self, gui_manager: pygame_gui.UIManager):

        layout_rect = pygame.Rect(0, 0, 100, 20)
        layout_rect.bottomleft = (-30, 0)

        self.hp_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=layout_rect,
            text="100",
            manager=gui_manager,
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'}
        )


    def update(self, new_hp: str):
        """
        Update the displayed health number
        """
        self.hp_label.text = new_hp
        self.hp_label.rebuild()
