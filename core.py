import pygame
from engine.game_manager import GameManager
from engine.state_machine import StateMachine
from engine.states.state_ids import StateID
from engine.utils.exceptions import GameExitException

# Import all state classes
from engine.states.main_menu_state import MainMenuState
from engine.states.campaign_select_state import CampaignSelectState
from engine.states.load_game_state import LoadGameState
from engine.states.settings_state import SettingsState
from engine.states.campaign_state import CampaignState
from engine.states.gameplay_state import GameplayState
from engine.states.victory_state import VictoryState


def launch_game():
    """Main entry point with State Machine"""
    game_manager = GameManager()
    config = game_manager.get_config()
    clock = pygame.time.Clock()
    
    state_machine = StateMachine(game_manager)
    
    # Register States
    state_machine.register_state(StateID.MAIN_MENU, MainMenuState)
    state_machine.register_state(StateID.CAMPAIGN_SELECT, CampaignSelectState)
    state_machine.register_state(StateID.LOAD_GAME, LoadGameState)
    state_machine.register_state(StateID.SETTINGS, SettingsState)
    state_machine.register_state(StateID.CAMPAIGN, CampaignState)
    state_machine.register_state(StateID.GAMEPLAY, GameplayState)
    state_machine.register_state(StateID.VICTORY, VictoryState)

    # Start with Main Menu
    state_machine.change_state(StateID.MAIN_MENU)

    running = True

    print("Game started")

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
                
            try:
                state_machine.handle_event(event)
            except GameExitException:
                running = False
                break

        if not running:
            break

        # Update
        time_delta = clock.tick(60) / 1000.0
        state_machine.update(time_delta)

        # Render
        # TODO: Currently the render method is superflous, and could just be called from the update method, but it's theoretically nice to be able to call them independantly.
        state_machine.render(time_delta)  
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    launch_game()
