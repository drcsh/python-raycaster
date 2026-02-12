import pygame
import pygame_gui
from engine.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.main_menu.main_menu_screen import MainMenuScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from engine.utils.exceptions import GameExitException

from typing import Optional

class MainMenuState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.menu_screen = None

    def enter(self):
        self.menu_screen = MainMenuScreen(
            self.game_manager.gui_manager,
            self.game_manager.get_config().resolution_width,
            self.game_manager.get_config().resolution_height
        )

    def exit(self):
        if self.menu_screen:
            self.menu_screen.cleanup()
            self.menu_screen = None

    def update(self, dt: float) -> Optional[StateTransition]:
        if self.menu_screen:
            self.menu_screen.update(dt)
        return None

    def render(self, time_delta: float):
        if self.menu_screen:
            self.menu_screen.draw(
                self.game_manager.display_surface,
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event) -> Optional[StateTransition]:
        self.game_manager.gui_manager.process_events(event)
        if self.menu_screen:
            action, result = self.menu_screen.handle_event(event)
            
            if action:
                if result == MainMenuAction.NEW_GAME:
                    return StateTransition(StateID.CAMPAIGN_SELECT)
                elif result == MainMenuAction.LOAD_GAME:
                    return StateTransition(StateID.LOAD_GAME)
                elif result == MainMenuAction.SETTINGS:
                    return StateTransition(StateID.SETTINGS)
                elif result == MainMenuAction.EXIT:
                    raise GameExitException("Exiting from Main Menu")
        return None
