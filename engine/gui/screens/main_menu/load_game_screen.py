from typing import Any, Optional

import pygame
import pygame_gui

from engine.gui.screens.base_screen import BaseScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from engine.gui.components.menu_button import MenuButton
from engine.gui.components.selectable_list import SelectableList


class LoadGameScreen(BaseScreen):
    """
    Screen for loading saved games.

    Currently a placeholder - shows empty list with message.
    """

    def __init__(self, gui_manager: pygame_gui.UIManager,
                 screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.save_list: Optional[SelectableList] = None
        self.back_button: Optional[MenuButton] = None
        super().__init__(gui_manager)

    def _create_ui_elements(self):
        """Create load game UI elements"""
        center_x = self.screen_width // 2

        # Title
        title_rect = pygame.Rect(0, 0, 400, 50)
        title_rect.center = (center_x, 100)
        title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="LOAD GAME",
            manager=self.gui_manager
        )
        self.ui_elements.append(title)

        # Placeholder list area
        list_rect = pygame.Rect(0, 0, 400, 300)
        list_rect.center = (center_x, 300)

        # Empty list with placeholder
        self.save_list = SelectableList(
            self.gui_manager,
            [],  # No saves yet
            list_rect
        )
        self.ui_elements.extend(self.save_list.ui_elements)

        # "No saves found" message
        message_rect = pygame.Rect(0, 0, 400, 40)
        message_rect.center = (center_x, 300)
        message = pygame_gui.elements.UILabel(
            relative_rect=message_rect,
            text="No saved games found",
            manager=self.gui_manager
        )
        self.ui_elements.append(message)

        # Return to Main Menu button
        self.back_button = MenuButton(
            self.gui_manager, "Return to Main Menu", center_x, 500
        )
        self.ui_elements.append(self.back_button.button)

    def _handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """Handle events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.back_button.is_clicked(event):
                return (True, MainMenuAction.SHOW_MAIN_MENU)
        return (False, None)

    def _cleanup(self):
        if self.save_list:
            self.save_list.kill()
        if self.back_button:
            self.back_button.kill()
        super()._cleanup()
