from engine.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.asset_loaders.campaign_loader import CampaignLoader
from typing import Optional

class CampaignState(State):
    """
    Campaign State acts as a controller for the campaign.
    It initiates the first level and holds the campaign progress.
    It transitions immediately to GameplayState.
    """
    def __init__(self, game_manager, campaign_path):
        super().__init__(game_manager)
        self.campaign_path = campaign_path
        self.campaign = None
        self.player_health = 100
        self.pending_start = False

    def enter(self):
        if not self.campaign:
            self.campaign = CampaignLoader.load_campaign(self.campaign_path)
            self.player_health = self.campaign.settings.get('starting_health', 100)
            self.pending_start = True

    def update(self, dt: float) -> Optional[StateTransition]:
        if self.pending_start:
            self.pending_start = False
            return self.get_gameplay_transition()
        return None

    def get_gameplay_transition(self) -> StateTransition:
        if self.campaign.is_complete():
            print("Campaign Complete!")
            return StateTransition(StateID.MAIN_MENU)

        level_data = self.campaign.get_current_level_data()
        
        return StateTransition(
            StateID.GAMEPLAY,
            kwargs={
                'level_data': level_data,
                'player_health': self.player_health,
                'campaign_state': self
            }
        )

    def on_level_complete(self, player_health: int) -> bool:
        """
        Updates player health and advances level.
        Returns True if campaign is still ongoing, False if complete.
        """
        self.player_health = player_health
        return self.campaign.advance_to_next_level()
        
    def is_complete(self) -> bool:
        return self.campaign.is_complete()

    def render(self, surface, time_delta: float):
        pass

    def handle_event(self, event) -> Optional[StateTransition]:
        return None
