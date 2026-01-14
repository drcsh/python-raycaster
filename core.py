import math
import numpy as np
from timeit import default_timer as timer
import pygame
import pygame_gui

from engine.campaign_loader import CampaignLoader
from engine.level_objects.map_loader import MapLoader
from engine.levelstate import LevelManager
from engine.gui.hud.hud import HUD
from engine.gui.screens.victory_screen import VictoryScreen
from engine.utils.exceptions import GameExitException, PlayerDeadException, LevelCompleteException
from engine.player_objects.input_handler import InputHandler
from engine.level_objects.level import Level
from engine.player_objects.player import Player
from engine.raycaster import RayCaster


def bootstrap():
    """
    Initialize pygame and create display/GUI objects

    Returns:
        tuple: (display_surface, background_surface, gui_manager, win_w, win_h, fov, dev_mode)
    """
    dev_mode = False
    win_w = 1024
    win_h = 628
    fov = math.pi / 3  # fov is expressed as a fraction of pi

    if dev_mode:
        win_w = win_w * 2

    # Pygame Setup
    pygame.init()
    pygame.key.set_repeat(100, 50)
    display_surface = pygame.display.set_mode([win_w, win_h])
    background_surface = pygame.Surface([win_w, win_h])

    # General Setup
    gui_manager = pygame_gui.UIManager((win_w, win_h))

    return display_surface, background_surface, gui_manager, win_w, win_h, fov, dev_mode


def load_level(level_data: dict, player_health: int, fov: float,
               display_surface: pygame.Surface, gui_manager: pygame_gui.UIManager,
               dev_mode: bool):
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
    level = MapLoader.create_level_from_data(level_data)

    # Create player at spawn position
    spawn = level_data['player_spawn']
    player = Player(spawn['x'], spawn['y'], spawn['angle'])
    player.hp = player_health

    # Create game objects
    raycaster = RayCaster(display_surface, level, fov, dev_mode=dev_mode)
    level_state = LevelManager(player, level)
    hud = HUD(level_state, gui_manager)

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


def run_campaign(campaign_path: str, display_surface: pygame.Surface,
                 background_surface: pygame.Surface, gui_manager: pygame_gui.UIManager,
                 fov: float, dev_mode: bool):
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
            level_data, player_health, fov, display_surface, gui_manager, dev_mode
        )

        input_handler = InputHandler(level_state, gui_manager)

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
                gui_manager.update(time_delta)

                pygame.display.flip()
                display_surface.blit(background_surface, (0, 0))

                gui_manager.draw_ui(display_surface)

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
            victory_screen = VictoryScreen(gui_manager, level_name, stats)

            if not victory_screen.show(display_surface, background_surface, clock):
                # User quit during victory screen
                print("Exiting during victory screen")
                return

            # Save player health
            player_health = player.hp

            # Advance campaign
            if not campaign.advance_to_next_level():
                # Campaign complete!
                show_campaign_complete_screen(gui_manager, display_surface,
                                            background_surface, clock, campaign)
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
    """Main entry point"""
    # Initialize pygame
    display_surface, background_surface, gui_manager, win_w, win_h, fov, dev_mode = bootstrap()

    # Run campaign
    campaign_path = "maps/campaigns/default_campaign/campaign.json"
    run_campaign(campaign_path, display_surface, background_surface,
                 gui_manager, fov, dev_mode)

    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    launch_game()
