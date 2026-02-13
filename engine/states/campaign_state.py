from engine.campaign import Campaign
from engine.game_manager import GameManager
from engine.states.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.asset_loaders.campaign_loader import CampaignLoader
from typing import Optional

class CampaignState(State):
    """
    Campaign State is a transitory state which handles campaign set up and progression.
    
    Providing the campaign_path will cause it to load the campaign from file and hand over to the GamePlay state. 
    Providing the campaign object will cause it to transition the campaign to the next level if there is one, or end the campaign if there isn't one.
    
    If neither campaign_path nor campaign are provided, it raises an exception.
    """
    def __init__(self, game_manager: GameManager, campaign_path : Optional[str] = None, campaign: Optional[Campaign] = None, player_health : Optional[int] = 100):
        super().__init__(game_manager)
        self.campaign_path = campaign_path
        self.campaign = campaign
        self.player_health = player_health
        self.pending_start = False

    def enter(self):
        if self.campaign: # Existing campaign
            self.campaign.advance_to_next_level()
            
        elif self.campaign_path: # New Campaign
            self.campaign = CampaignLoader.load_campaign(self.campaign_path)
            self.player_health = self.campaign.settings.get('starting_health', 100)
            self.pending_start = True

        else:
            raise ValueError("CampaignState entered without data to create campaign! This shouldn't happen!")

    def update(self, dt: float) -> Optional[StateTransition]:
        return self.get_gameplay_transition()

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
                'campaign': self.campaign
            }
        )
        
    def render(self, time_delta: float):
        pass

    def handle_event(self, event) -> Optional[StateTransition]:
        return None
