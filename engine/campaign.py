import os
from typing import List, Dict
from engine.asset_loaders.level_loader import LevelLoader


class Campaign:
    """
    Manages campaign state and progression through levels

    Responsibilities:
    - Track current level index in campaign
    - Manage campaign state (progress, current level)
    - Provide methods to navigate through levels
    - Support serialization for save/load (future)
    - Detect campaign completion
    """

    def __init__(self, campaign_data: dict, campaign_dir: str, levels_directory: str):
        """
        Initialize campaign with parsed data

        Args:
            campaign_data: Parsed campaign JSON data
            campaign_dir: Directory containing campaign.json
            levels_directory: Subdirectory name containing level files
        """
        # Store campaign metadata (read-only)
        self.campaign_id = campaign_data['campaign_id']
        self.name = campaign_data.get('name', 'Unnamed Campaign')
        self.description = campaign_data.get('description', '')
        self.author = campaign_data.get('author', 'Unknown')
        self.difficulty = campaign_data.get('difficulty', 'medium')

        # Store path information
        self.campaign_dir = campaign_dir
        self.levels_directory = levels_directory

        # Store level list
        self.levels = campaign_data['levels']

        # Store settings
        self.settings = campaign_data.get('settings', {})

        # Initialize mutable state
        self.current_level_index = 0

    def get_current_level_data(self) -> dict:
        """
        Return data for current level

        Returns:
            dict: Level data loaded from JSON

        Raises:
            IndexError: If current_level_index is out of range
        """
        if self.current_level_index >= len(self.levels):
            raise IndexError(f"Level index {self.current_level_index} out of range")

        level_entry = self.levels[self.current_level_index]
        level_filename = level_entry['level_file']

        # Construct full path to level file
        level_path = self.get_current_level_path()

        # Load and return level data
        return LevelLoader.load_level(level_path)

    def get_current_level_path(self) -> str:
        """
        Return full path to current level JSON file

        Returns:
            str: Absolute path to level file
        """
        if self.current_level_index >= len(self.levels):
            raise IndexError(f"Level index {self.current_level_index} out of range")

        level_entry = self.levels[self.current_level_index]
        level_filename = level_entry['level_file']

        # Construct full path: campaign_dir / levels_directory / level_file
        level_path = os.path.join(self.campaign_dir, self.levels_directory, level_filename)

        return level_path

    def advance_to_next_level(self) -> bool:
        """
        Move to next level, return False if campaign complete

        Returns:
            bool: True if more levels exist, False if campaign complete
        """
        self.current_level_index += 1

        if self.current_level_index >= len(self.levels):
            return False  # Campaign complete

        return True  # More levels available

    def is_complete(self) -> bool:
        """
        Check if all levels completed

        Returns:
            bool: True if campaign is complete
        """
        return self.current_level_index >= len(self.levels)

    def reset(self):
        """Reset campaign to beginning (current_level_index = 0)"""
        self.current_level_index = 0

    def to_dict(self) -> dict:
        """
        Serialize campaign state to dict (for future save system)

        Returns:
            dict: Campaign state suitable for JSON serialization
        """
        return {
            'campaign_id': self.campaign_id,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'difficulty': self.difficulty,
            'campaign_dir': self.campaign_dir,
            'levels_directory': self.levels_directory,
            'levels': self.levels,
            'settings': self.settings,
            'current_level_index': self.current_level_index
        }
