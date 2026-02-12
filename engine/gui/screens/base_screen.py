from abc import ABC, abstractmethod
from typing import Any

import pygame
import pygame_gui

from engine.gui.screens.main_menu.menu_action import MainMenuAction


class BaseScreen(ABC):
    """
    Abstract base class for menu screens.

    Provides common functionality:
    - UI element management
    - Event loop structure
    - Cleanup handling
    """

    def __init__(self, gui_manager: pygame_gui.UIManager):
        self.gui_manager = gui_manager
        self.ui_elements = []
        self._create_ui_elements()

    @abstractmethod
    def _create_ui_elements(self):
        """Create UI elements for this screen. Subclasses must implement."""
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """
        Handle a single event.

        Returns:
            tuple: (should_exit, result_value)
                - should_exit: True if the screen should close
                - result_value: Value to return (e.g. MenuAction)
        """
        pass

    def update(self, time_delta: float):
        """Update the UI"""
        self.gui_manager.update(time_delta)

    def draw(self, display_surface: pygame.Surface, background_surface: pygame.Surface = None):
        """Draw the UI"""
        if background_surface:
             display_surface.blit(background_surface, (0, 0))
        self.gui_manager.draw_ui(display_surface)

    def cleanup(self):
        """Remove all UI elements"""
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()

