import json
import os
from engine.campaign import Campaign


class CampaignLoader:
    """Static utility class for loading campaigns from JSON files"""

    @staticmethod
    def load_campaign(campaign_file_path: str) -> Campaign:
        """
        Load campaign from JSON file and return Campaign object

        Args:
            campaign_file_path: Full path to campaign.json file

        Returns:
            Campaign: Initialized Campaign object

        Raises:
            FileNotFoundError: If campaign file doesn't exist
            json.JSONDecodeError: If JSON is malformed
            ValueError: If campaign data is invalid
        """
        if not os.path.exists(campaign_file_path):
            raise FileNotFoundError(f"Campaign file not found: {campaign_file_path}")

        try:
            with open(campaign_file_path, 'r') as f:
                campaign_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in campaign file {campaign_file_path}: {e.msg}",
                e.doc,
                e.pos
            )

        # Validate the loaded data
        CampaignLoader.validate_campaign_data(campaign_data)

        # Get campaign directory (parent directory of campaign.json)
        campaign_dir = os.path.dirname(os.path.abspath(campaign_file_path))

        # Get levels directory (defaults to "levels")
        levels_directory = campaign_data.get('levels_directory', 'levels')

        # Create and return Campaign object
        return Campaign(campaign_data, campaign_dir, levels_directory)

    @staticmethod
    def validate_campaign_data(campaign_data: dict) -> bool:
        """
        Validate campaign data structure

        Args:
            campaign_data: Dict containing campaign data

        Returns:
            bool: True if valid

        Raises:
            ValueError: If campaign data is invalid
        """
        # Check required fields
        required_fields = ['campaign_id', 'name', 'levels']
        for field in required_fields:
            if field not in campaign_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate levels array
        if not isinstance(campaign_data['levels'], list):
            raise ValueError("'levels' must be a list")

        if len(campaign_data['levels']) == 0:
            raise ValueError("Campaign must have at least one level")

        # Validate each level entry
        for i, level_entry in enumerate(campaign_data['levels']):
            if not isinstance(level_entry, dict):
                raise ValueError(f"Level entry {i} must be a dict")

            if 'level_file' not in level_entry:
                raise ValueError(f"Level entry {i}: missing 'level_file' field")

        # Validate settings if present
        if 'settings' in campaign_data:
            if not isinstance(campaign_data['settings'], dict):
                raise ValueError("'settings' must be a dict")

        return True
