import pygame
import pygame_gui

from engine.config.config_data import Config
from engine.asset_loaders.config_loader import ConfigLoader
CONFIG_PATH = 'config.json'


class GameManager:
    """
    The GameManager initializes and keeps track of key dependencies needed to run the game. 

    Its purpose is to provide one place to initialize key dependencies and to avoid the need to pass multiple objects around between classes.

    TODO: turn this into an adapter for PyGame, abstracting away how Pygame works from the game state machine.
    """
    def __init__(self):
        # Load configuration
        self._config: Config = ConfigLoader.load_config(CONFIG_PATH)
        self.dev_mode: bool = self._config.dev_mode
        
        # Pygame Setup
        pygame.init()
        pygame.key.set_repeat(100, 50)
        self.display_surface = pygame.display.set_mode([self._config.resolution_width, self._config.resolution_height])
        self.background_surface = pygame.Surface([self._config.resolution_width, self._config.resolution_height])

        # General Setup
        self.gui_manager = pygame_gui.UIManager((self._config.resolution_width, self._config.resolution_height))
        self.field_of_view = self._config.field_of_view * (3.14159265 / 180)  # Convert degrees to radians

    def get_config(self) -> Config:
        """Return the configuration dataclass"""
        return self._config
