from engine.campaign_manager import CampaignManager
from engine.game_manager import GameManager
from engine.states.state_machine import State, StateTransition
from engine.states.state_ids import StateID
from engine.asset_loaders.campaign_loader import CampaignLoader
from typing import Optional

class CampaignState(State):
    """
    Campaign State is a transitory state which handles campaign set up and progression.
    
    Providing the campaign_path will cause it to load the campaign from file and hand over to the GamePlay state. 
    Providing the campaign_manager will cause it to transition the campaign to the next level if there is one, or end the campaign if there isn't one.
    
    If neither campaign_path nor campaign_manager are provided, it raises an exception.
    """
    def __init__(self, game_manager: GameManager, campaign_path : Optional[str] = None, campaign_manager: Optional[CampaignManager] = None):
        super().__init__(game_manager)
        self.campaign_path = campaign_path
        self.campaign_manager = campaign_manager
        self.pending_start = False

    def enter(self):
        if self.campaign_manager: # Existing campaign
            self.campaign_manager.advance_to_next_level()
            
        elif self.campaign_path: # New Campaign
            self.campaign_manager = CampaignLoader.load_campaign(self.campaign_path)
            self.pending_start = True

        else:
            raise ValueError("CampaignState entered without data to create campaign! This shouldn't happen!")

    def update(self, dt: float) -> Optional[StateTransition]:
        return self.get_gameplay_transition()

    def get_gameplay_transition(self) -> StateTransition:
        if self.campaign_manager.is_complete():
            print("Campaign Complete!")
            return StateTransition(StateID.MAIN_MENU)
        
        return StateTransition(
            StateID.GAMEPLAY,
            kwargs={
                'campaign_manager': self.campaign_manager
            }
        )
        
    def render(self, time_delta: float):
        pass

    def handle_event(self, event) -> Optional[StateTransition]:
        return None
