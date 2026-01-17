from typing import Any

import pygame
import pygame_gui

from engine.gui.screens.base_screen import BaseScreen
from engine.gui.screens.menu_action import MenuAction
from engine.gui.components.menu_button import MenuButton


class MainMenuScreen(BaseScreen):
    """
    Main menu screen with New Game, Load Game, Settings, and Exit options.
    """

    def __init__(self, gui_manager: pygame_gui.UIManager,
                 screen_width: int, screen_height: int):
        """
        Initialize main menu.

        Args:
            gui_manager: pygame_gui UIManager instance
            screen_width: Screen width for centering elements
            screen_height: Screen height for positioning
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons: dict[str, tuple[MenuButton, MenuAction]] = {}
        super().__init__(gui_manager)

    def _create_ui_elements(self):
        """Create main menu UI elements"""
        center_x = self.screen_width // 2

        # Title
        title_rect = pygame.Rect(0, 0, 500, 80)
        title_rect.center = (center_x, 150)
        title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="PYTHON RAYCASTER",
            manager=self.gui_manager
        )
        self.ui_elements.append(title)

        # Menu buttons - vertically centered with spacing
        button_start_y = 280
        button_spacing = 70

        button_configs = [
            ("new_game", "New Game", MenuAction.NEW_GAME),
            ("load_game", "Load Game", MenuAction.LOAD_GAME),
            ("settings", "Settings", MenuAction.SETTINGS),
            ("exit", "Exit", MenuAction.EXIT),
        ]

        for i, (key, text, action) in enumerate(button_configs):
            y = button_start_y + (i * button_spacing)
            btn = MenuButton(self.gui_manager, text, center_x, y)
            self.buttons[key] = (btn, action)
            self.ui_elements.append(btn.button)

    def _handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """Handle button clicks"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for key, (btn, action) in self.buttons.items():
                if btn.is_clicked(event):
                    return (True, action)
        return (False, None)

    def _cleanup(self):
        """Clean up buttons and UI elements"""
        for key, (btn, action) in self.buttons.items():
            btn.kill()
        self.buttons.clear()
        super()._cleanup()
