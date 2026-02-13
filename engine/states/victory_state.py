import pygame
from engine.campaign_manager import CampaignManager
from engine.entities.player import Player
from engine.game_manager import GameManager
from engine.level_manager import LevelManager
from engine.states.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.victory_screen import VictoryScreen
from engine.utils.exceptions import GameExitException

class VictoryState(State):
    def __init__(self, game_manager: GameManager, level_manager: LevelManager, campaign_manager: CampaignManager):
        super().__init__(game_manager)
        self.game_manager = game_manager
        self.level_manager = level_manager
        self.campaign_manager = campaign_manager
        self.victory_screen = None

    def enter(self):
        self.victory_screen = VictoryScreen(
            self.game_manager.gui_manager,
            self.level_manager.level.name,
            self.level_manager.level.get_completion_stats()
        )

    def exit(self):
        if self.victory_screen:
            self.victory_screen.cleanup()
            self.victory_screen = None

    def update(self, dt: float):
        if self.victory_screen:
            self.victory_screen.update(dt)

    def render(self, time_delta: float):
        if self.victory_screen:
            self.victory_screen.draw(
                self.game_manager.display_surface, 
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event):
        self.game_manager.gui_manager.process_events(event)
        if self.victory_screen:
            should_continue = self.victory_screen.handle_event(event)
            
            if should_continue:
                # Proceed to next level
                return StateTransition(StateID.CAMPAIGN, kwargs={
                    'campaign_manager': self.campaign_manager
                })
