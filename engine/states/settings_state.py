import pygame
import pygame_gui
from engine.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.main_menu.settings_screen import SettingsScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from typing import Optional

class SettingsState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.settings_screen = None

    def enter(self):
        self.settings_screen = SettingsScreen(
            self.game_manager.gui_manager,
            self.game_manager.get_config().resolution_width,
            self.game_manager.get_config().resolution_height,
            self.game_manager.get_config()
        )

    def exit(self):
        if self.settings_screen:
            self.settings_screen.cleanup()
            self.settings_screen = None

    def update(self, dt: float) -> Optional[StateTransition]:
        if self.settings_screen:
            self.settings_screen.update(dt)
        return None

    def render(self, surface: pygame.Surface, time_delta: float):
        if self.settings_screen:
            self.settings_screen.draw(
                surface, 
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event) -> Optional[StateTransition]:
        self.game_manager.gui_manager.process_events(event)
        if self.settings_screen:
            action, result = self.settings_screen.handle_event(event)

            if action:
                if result == MainMenuAction.SHOW_MAIN_MENU:
                    return StateTransition(StateID.MAIN_MENU)
        return None
