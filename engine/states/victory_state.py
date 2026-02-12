import pygame
from engine.campaign import Campaign
from engine.entities.player import Player
from engine.game_manager import GameManager
from engine.level_manager import LevelManager
from engine.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.gui.screens.victory_screen import VictoryScreen
from engine.utils.exceptions import GameExitException

class VictoryState(State):
    def __init__(self, game_manager: GameManager, level: LevelManager, level_data: dict, campaign: Campaign, player: Player):
        super().__init__(game_manager)
        self.game_manager = game_manager
        self.level = level
        self.level_data = level_data
        self.campaign = campaign
        self.player = player
        self.victory_screen = None

    def enter(self):
        # Calculate stats
        stats = self.level.get_completion_stats()
        level_name = self.level_data.get('name', 'Unknown Level')
        
        self.victory_screen = VictoryScreen(
            self.game_manager.gui_manager,
            level_name,
            stats
        )

    def exit(self):
        if self.victory_screen:
            self.victory_screen.cleanup()
            self.victory_screen = None

    def update(self, dt: float):
        if self.victory_screen:
            self.victory_screen.update(dt)

    def render(self, surface: pygame.Surface, time_delta: float):
        if self.victory_screen:
            self.victory_screen.draw(
                surface, 
                self.game_manager.background_surface
            )

    def handle_event(self, event: pygame.event.Event):
        self.game_manager.gui_manager.process_events(event)
        if self.victory_screen:
            should_continue = self.victory_screen.handle_event(event)
            
            if should_continue:
                # Proceed to next level
                return StateTransition(StateID.CAMPAIGN, kwargs={
                    'player_health': self.player.hp,
                    'campaign': self.campaign
                })
