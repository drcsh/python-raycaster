from typing import Any, Optional

import pygame
import pygame_gui

from engine.gui.screens.base_screen import BaseScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from engine.gui.components.menu_button import MenuButton
from engine.config.config_data import Config


class SettingsScreen(BaseScreen):
    """
    Screen for displaying current settings.

    Shows settings from Config dataclass (read-only for now).
    """

    def __init__(self, gui_manager: pygame_gui.UIManager,
                 screen_width: int, screen_height: int,
                 config: Config):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config = config
        self.back_button: Optional[MenuButton] = None
        super().__init__(gui_manager)

    def _create_ui_elements(self):
        """Create settings display UI elements"""
        center_x = self.screen_width // 2

        # Title
        title_rect = pygame.Rect(0, 0, 400, 50)
        title_rect.center = (center_x, 100)
        title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="SETTINGS",
            manager=self.gui_manager
        )
        self.ui_elements.append(title)

        # Settings display
        settings_text = self._format_settings()

        settings_rect = pygame.Rect(0, 0, 500, 250)
        settings_rect.center = (center_x, 300)
        settings_box = pygame_gui.elements.UITextBox(
            html_text=settings_text,
            relative_rect=settings_rect,
            manager=self.gui_manager
        )
        self.ui_elements.append(settings_box)

        # Return to Main Menu button
        self.back_button = MenuButton(
            self.gui_manager, "Return to Main Menu", center_x, 500
        )
        self.ui_elements.append(self.back_button.button)

    def _format_settings(self) -> str:
        """Format settings for display"""
        return (
            f"<b>Resolution:</b> {self.config.resolution_width} x {self.config.resolution_height}<br>"
            f"<b>Field of View:</b> {self.config.field_of_view} degrees<br>"
            f"<b>Developer Mode:</b> {'Enabled' if self.config.dev_mode else 'Disabled'}"
        )

    def _handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """Handle events"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.back_button.is_clicked(event):
                return (True, MainMenuAction.SHOW_MAIN_MENU)
        return (False, None)

    def _cleanup(self):
        if self.back_button:
            self.back_button.kill()
        super()._cleanup()
