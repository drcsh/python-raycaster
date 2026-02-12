import pygame
import numpy as np
from timeit import default_timer as timer

from engine.state_machine import State, StateTransition
from engine.asset_loaders.level_loader import LevelLoader
from engine.game_manager import GameManager
from engine.level_manager import LevelManager
from engine.states.state_ids import StateID
from engine.states.campaign_state import CampaignState
from engine.gui.hud.hud import HUD
from engine.input.input_handler import InputHandler
from engine.entities.player import Player
from engine.raycaster import RayCaster
from engine.utils.exceptions import GameExitException, PlayerDeadException, LevelCompleteException

from typing import Optional

class GameplayState(State):
    def __init__(self, game_manager: GameManager, level_data: dict, player_health: int, campaign_state: CampaignState):
        self.game_manager = game_manager
        self.level_data = level_data
        self.player_health = player_health
        self.campaign_state = campaign_state
        
        # Game objects
        self.level = None
        self.player = None
        self.level_state = None
        self.raycaster = None
        self.hud = None
        self.input_handler = None
        self.clock = pygame.time.Clock()

    def enter(self):
        # Create level using MapLoader
        self.level = LevelLoader.create_level_from_data(self.level_data)

        # Create player at spawn position
        spawn = self.level_data['player_spawn']
        self.player = Player(spawn['x'], spawn['y'], spawn['angle'])
        self.player.hp = self.player_health

        # Create game objects
        self.raycaster = RayCaster(
            display_surface=self.game_manager.display_surface, 
            level=self.level, 
            fov=self.game_manager.field_of_view, 
            dev_mode=self.game_manager.dev_mode
        )
        self.level_state = LevelManager(self.player, self.level)
        self.hud = HUD(self.level_state, self.game_manager.gui_manager)
        self.input_handler = InputHandler(self.level_state, self.game_manager.gui_manager)

        # Performance tracking (optional, keeping it simple for now)
        self.caster_ts = []

    def exit(self):
        # Clean up if needed
        pass

    def update(self, dt: float) -> Optional[StateTransition]:
        try:
            self.level_state.trigger_all_behaviours()
            self.hud.update()
            
            # The gui_manager update is handled here as well as it might need time updates?
            # Actually GameManager.gui_manager is updated in the unified core loop if I put it there?
            # No, I should update it here because State loop calls state.update()
            # But wait, BaseScreen.update calls gui_manager.update().
            # Here handle_event does process_events.
            
        except LevelCompleteException:
            # Transition to VictoryState
            from engine.states.victory_state import VictoryState
            return StateTransition(StateID.VICTORY, kwargs={
                'level': self.level, 
                'level_data': self.level_data, 
                'campaign_state': self.campaign_state,
                'player': self.player
            })

        except PlayerDeadException:
            return StateTransition(StateID.MAIN_MENU)

        except GameExitException:
            return StateTransition(StateID.MAIN_MENU)

    def render(self, surface: pygame.Surface, time_delta: float):
        # Clear the screen
        self.game_manager.display_surface.blit(self.game_manager.background_surface, (0, 0))

        # RayCaster renders everything.
        self.raycaster.cast(self.player.x, self.player.y, self.player.angle)
        self.raycaster.render_game_objects(self.player.x, self.player.y, self.player.angle)
        
         # Update the UI
        self.hud.update()
        self.game_manager.gui_manager.update(time_delta)

        self.game_manager.gui_manager.draw_ui(self.game_manager.display_surface)


    def handle_event(self, event: pygame.event.Event):
        try:
            self.input_handler.process_event(event)
        except GameExitException:
            from engine.states.main_menu_state import MainMenuState
            self.state_machine.change_state(MainMenuState(self.state_machine, self.game_manager))
