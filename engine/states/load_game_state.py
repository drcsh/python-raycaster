import pygame
import pygame_gui
from engine.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.main_menu.load_game_screen import LoadGameScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from typing import Optional

class LoadGameState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.load_screen = None

    def enter(self):
        self.load_screen = LoadGameScreen(
            self.game_manager.gui_manager,
            self.game_manager.get_config().resolution_width,
            self.game_manager.get_config().resolution_height
        )

    def exit(self):
        if self.load_screen:
            self.load_screen.cleanup()
            self.load_screen = None

    def update(self, dt: float) -> Optional[StateTransition]:
        if self.load_screen:
            self.load_screen.update(dt)
        return None

    def render(self, surface: pygame.Surface, time_delta: float):
        if self.load_screen:
            self.load_screen.draw(
                surface, 
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event) -> Optional[StateTransition]:
        self.game_manager.gui_manager.process_events(event)
        if self.load_screen:
            action, result = self.load_screen.handle_event(event)

            if action:
                if result == MainMenuAction.SHOW_MAIN_MENU:
                    return StateTransition(StateID.MAIN_MENU)
        return None
