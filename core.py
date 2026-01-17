import math
import numpy as np
from timeit import default_timer as timer
import pygame
import pygame_gui

from engine.asset_loaders.campaign_loader import CampaignLoader
from engine.asset_loaders.level_loader import LevelLoader
from engine.game_manager import GameManager
from engine.level_manager import LevelManager
from engine.gui.hud.hud import HUD
from engine.gui.screens.victory_screen import VictoryScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from engine.gui.screens.main_menu.main_menu_screen import MainMenuScreen
from engine.gui.screens.main_menu.campaign_select_screen import CampaignSelectScreen
from engine.gui.screens.main_menu.load_game_screen import LoadGameScreen
from engine.gui.screens.main_menu.settings_screen import SettingsScreen
from engine.utils.exceptions import GameExitException, PlayerDeadException, LevelCompleteException
from engine.input.input_handler import InputHandler
from engine.level_objects.level import Level
from engine.entities.player import Player
from engine.raycaster import RayCaster



def load_level(level_data: dict, player_health: int, game_manager: GameManager):
    """
    Load a level from level data dict and return game objects

    Args:
        level_data: Parsed level JSON data
        player_health: Player's current health
        fov: Field of view in radians
        display_surface: Main display surface
        gui_manager: pygame_gui UIManager instance
        dev_mode: Whether developer mode is enabled

    Returns:
        tuple: (level, player, level_state, raycaster, hud)
    """
    # Create level using MapLoader
    level = LevelLoader.create_level_from_data(level_data)

    # Create player at spawn position
    spawn = level_data['player_spawn']
    player = Player(spawn['x'], spawn['y'], spawn['angle'])
    player.hp = player_health

    # Create game objects
    raycaster = RayCaster(display_surface=game_manager.display_surface, level=level, fov=game_manager.field_of_view, dev_mode=game_manager.dev_mode)
    level_state = LevelManager(player, level)
    hud = HUD(level_state, game_manager.gui_manager)

    return level, player, level_state, raycaster, hud


def show_campaign_complete_screen(gui_manager: pygame_gui.UIManager,
                                  display_surface: pygame.Surface,
                                  background_surface: pygame.Surface,
                                  clock: pygame.time.Clock,
                                  campaign):
    """
    Display campaign completion screen

    Args:
        gui_manager: pygame_gui UIManager instance
        display_surface: Main display surface
        background_surface: Background surface
        clock: Pygame clock
        campaign: Campaign object
    """
    # Create a simple completion screen using VictoryScreen
    stats = {
        "enemies_defeated": 0,
        "total_enemies": 0,
        "time_elapsed": 0
    }
    completion_screen = VictoryScreen(
        gui_manager,
        f"Campaign Complete: {campaign.name}",
        stats
    )
    completion_screen.show(display_surface, background_surface, clock)


def run_campaign(campaign_path: str, game_manager: GameManager):
    """
    Run a campaign from start to finish

    Args:
        campaign_path: Path to campaign.json file
        display_surface: Main display surface
        background_surface: Background surface
        gui_manager: pygame_gui UIManager instance
        fov: Field of view in radians
        dev_mode: Whether developer mode is enabled
    """
    # Load campaign using CampaignLoader
    campaign = CampaignLoader.load_campaign(campaign_path)

    # Get starting health from campaign settings
    player_health = campaign.settings.get('starting_health', 100)

    clock = pygame.time.Clock()

    # Performance tracking
    caster_ts = []
    caster_worst = -1
    caster_best = 10

    # Main campaign loop
    while not campaign.is_complete():
        # Load current level
        level_data = campaign.get_current_level_data()
        level, player, level_state, raycaster, hud = load_level(
            level_data, player_health, game_manager
        )

        input_handler = InputHandler(level_state, game_manager.gui_manager)

        # Reset performance tracking for this level
        level_caster_ts = []
        time_delta = 0

        # Level game loop
        try:
            while True:
                input_handler.handle()
                level_state.trigger_all_behaviours()

                # Render the scene
                start = timer()
                raycaster.cast(player.x, player.y, player.angle)
                raycaster.render_game_objects(player.x, player.y, player.angle)
                end = timer()

                level_caster_ts.append(end - start)

                # Update the UI
                hud.update()
                game_manager.gui_manager.update(time_delta)

                pygame.display.flip()
                game_manager.display_surface.blit(game_manager.background_surface, (0, 0))

                game_manager.gui_manager.draw_ui(game_manager.display_surface)

                if len(level_caster_ts) > 100:  # stop list becoming too long
                    av = np.average(level_caster_ts)
                    print(f"Caster avg cast time (last 100):{av}")
                    if av > caster_worst:
                        caster_worst = av
                    if av < caster_best:
                        caster_best = av
                    level_caster_ts = []

                # cap the framerate
                time_delta = clock.tick(60) / 1000.0

        except LevelCompleteException:
            # Add level performance stats to overall tracking
            caster_ts.extend(level_caster_ts)

            # Show victory screen
            stats = level.get_completion_stats()
            level_name = level_data.get('name', 'Unknown Level')
            victory_screen = VictoryScreen(game_manager.gui_manager, level_name, stats)

            if not victory_screen.show(game_manager.display_surface, game_manager.background_surface, clock):
                # User quit during victory screen
                print("Exiting during victory screen")
                return

            # Save player health
            player_health = player.hp

            # Advance campaign
            if not campaign.advance_to_next_level():
                # Campaign complete!
                show_campaign_complete_screen(game_manager.gui_manager, game_manager.display_surface,
                                            game_manager.background_surface, clock, campaign)
                break

        except PlayerDeadException as ex:
            print(f"Player Died! {ex}")
            break

        except GameExitException as ex:
            print(f"Exiting: {ex}")
            break

    # Print performance stats
    if caster_ts:
        print(f"Caster avg cast time (all levels):{np.average(caster_ts)}")
        print(f"Caster best avg cast time for 100 renders: {caster_best}")
        print(f"Caster worst avg cast time for 100 renders: {caster_worst}")


def launch_game():
    """Main entry point with main menu"""
    game_manager = GameManager()
    config = game_manager.get_config()
    clock = pygame.time.Clock()

    running = True

    action = MainMenuAction.SHOW_MAIN_MENU

    while running:
        # Show main menu
        
        if action == MainMenuAction.SHOW_MAIN_MENU:
            main_menu = MainMenuScreen(
                game_manager.gui_manager,
                config.resolution_width,
                config.resolution_height
            )
            action = main_menu.show(
                game_manager.display_surface,
                game_manager.background_surface,
                clock
            )

        elif action == MainMenuAction.NEW_GAME:
            # Show campaign selection
            campaign_screen = CampaignSelectScreen(
                game_manager.gui_manager,
                config.resolution_width,
                config.resolution_height
            )
            action = campaign_screen.show(
                game_manager.display_surface,
                game_manager.background_surface,
                clock
            )

            if action not in MainMenuAction.__members__.values():
                # action is a campaign path 
                #TODO: Make this nicer
                run_campaign(action, game_manager)

        elif action == MainMenuAction.LOAD_GAME:
            load_screen = LoadGameScreen(
                game_manager.gui_manager,
                config.resolution_width,
                config.resolution_height
            )
            action = load_screen.show(
                game_manager.display_surface,
                game_manager.background_surface,
                clock
            )

        elif action == MainMenuAction.SETTINGS:
            settings_screen = SettingsScreen(
                game_manager.gui_manager,
                config.resolution_width,
                config.resolution_height,
                config
            )
            action = settings_screen.show(
                game_manager.display_surface,
                game_manager.background_surface,
                clock
            )

        elif action == MainMenuAction.EXIT:
            running = False

    pygame.quit()


if __name__ == "__main__":
    launch_game()
