import pygame
import pygame_gui


class MenuButton:
    """
    Reusable styled button for menu screens.

    Provides consistent styling and positioning for menu buttons.
    """

    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 50

    def __init__(self,
                 gui_manager: pygame_gui.UIManager,
                 text: str,
                 center_x: int,
                 center_y: int,
                 width: int = DEFAULT_WIDTH,
                 height: int = DEFAULT_HEIGHT):
        """
        Create a menu button.

        Args:
            gui_manager: pygame_gui UIManager instance
            text: Button label text
            center_x: X coordinate of button center
            center_y: Y coordinate of button center
            width: Button width (default 300)
            height: Button height (default 50)
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)

        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=text,
            manager=gui_manager
        )

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """Check if this button was clicked in the given event"""
        return (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == self.button)

    def kill(self):
        """Remove the button from the UI"""
        self.button.kill()
