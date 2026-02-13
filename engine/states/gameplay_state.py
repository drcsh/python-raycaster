import pygame
import numpy as np
from timeit import default_timer as timer

from engine.campaign_manager import CampaignManager
from engine.states.state_machine import State, StateTransition
from engine.asset_loaders.level_loader import LevelLoader
from engine.game_manager import GameManager
from engine.level_manager import LevelManager
from engine.states.state_ids import StateID
from engine.gui.hud.hud import HUD
from engine.input.input_handler import InputHandler
from engine.entities.player import Player
from engine.raycaster import RayCaster
from engine.utils.exceptions import GameExitException, PlayerDeadException, LevelCompleteException

from typing import Optional

class GameplayState(State):
    def __init__(self, game_manager: GameManager, campaign_manager: CampaignManager):
        self.game_manager = game_manager
        self.campaign_manager = campaign_manager
        
        # Game objects
        self.level_manager = None
        self.raycaster = None
        self.hud = None
        self.input_handler = None
        self.clock = pygame.time.Clock()

    def enter(self):
        self.level_manager = self.campaign_manager.get_current_level_manager()

        # Create game objects
        self.raycaster = RayCaster(
            display_surface=self.game_manager.display_surface, 
            level=self.level_manager.level, 
            fov=self.game_manager.field_of_view, 
            dev_mode=self.game_manager.dev_mode
        )
        
        self.hud = HUD(self.level_manager, self.game_manager.gui_manager)
        self.input_handler = InputHandler(self.level_manager, self.game_manager.gui_manager)

        # Performance tracking (optional, keeping it simple for now)
        self.caster_ts = []

    def exit(self):
        # Clean up if needed
        pass

    def update(self, dt: float) -> Optional[StateTransition]:
        try:
            self.level_manager.trigger_all_behaviours()
            
        except LevelCompleteException:
            # Transition to VictoryState
            from engine.states.victory_state import VictoryState
            return StateTransition(StateID.VICTORY, kwargs={
                'level_manager': self.level_manager, 
                'campaign_manager': self.campaign_manager,
            })

        except PlayerDeadException:
            return StateTransition(StateID.MAIN_MENU)

        except GameExitException:
            return StateTransition(StateID.MAIN_MENU)

    def render(self, time_delta: float):
        # Clear the screen
        self.game_manager.display_surface.blit(self.game_manager.background_surface, (0, 0))

        # RayCaster renders everything.
        self.raycaster.cast(self.level_manager.player.x, self.level_manager.player.y, self.level_manager.player.angle)
        self.raycaster.render_game_objects(self.level_manager.player.x, self.level_manager.player.y, self.level_manager.player.angle)
        
         # Update the UI
        self.hud.update()
        self.game_manager.gui_manager.update(time_delta)

        self.game_manager.gui_manager.draw_ui(self.game_manager.display_surface)


    def handle_event(self, event: pygame.event.Event):
        try:
            self.input_handler.process_event(event)
        except GameExitException:
            return StateTransition(StateID.MAIN_MENU, kwargs={})
