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
    def _handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """
        Handle a single event.

        Returns:
            tuple: (should_exit, result_value)
                - should_exit: True if the screen should close
                - result_value: Value to return from show()
        """
        pass

    def show(self, display_surface: pygame.Surface,
             background_surface: pygame.Surface,
             clock: pygame.time.Clock) -> Any:
        """
        Display the screen and run event loop.

        Returns:
            Result value determined by subclass (e.g., MenuAction, campaign path)
        """
        running = True
        result = None
        time_delta = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._cleanup()
                    return MainMenuAction.EXIT

                # Let subclass handle the event
                should_exit, result = self._handle_event(event)
                if should_exit:
                    running = False
                    break

                self.gui_manager.process_events(event)

            # Update and draw
            self.gui_manager.update(time_delta)
            display_surface.blit(background_surface, (0, 0))
            self.gui_manager.draw_ui(display_surface)
            pygame.display.flip()

            time_delta = clock.tick(60) / 1000.0

        self._cleanup()
        return result

    def _cleanup(self):
        """Remove all UI elements"""
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()
