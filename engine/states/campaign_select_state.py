import pygame
from engine.states.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.main_menu.campaign_select_screen import CampaignSelectScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from typing import Optional

class CampaignSelectState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.campaign_screen = None

    def enter(self):
        self.campaign_screen = CampaignSelectScreen(
            self.game_manager.gui_manager,
            self.game_manager.get_config().resolution_width,
            self.game_manager.get_config().resolution_height
        )

    def exit(self):
        if self.campaign_screen:
            self.campaign_screen.cleanup()
            self.campaign_screen = None

    def update(self, dt: float) -> Optional[StateTransition]:
        if self.campaign_screen:
            self.campaign_screen.update(dt)
        return None

    def render(self, time_delta: float):
        if self.campaign_screen:
            self.campaign_screen.draw(
                self.game_manager.display_surface,
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event) -> Optional[StateTransition]:
        self.game_manager.gui_manager.process_events(event)
        if self.campaign_screen:
            action, result = self.campaign_screen.handle_event(event)
            
            if action:
                if result == MainMenuAction.SHOW_MAIN_MENU:
                    return StateTransition(StateID.MAIN_MENU)
                else:
                    # Result is campaign path
                    return StateTransition(StateID.CAMPAIGN, kwargs={'campaign_path': result})
        return None
