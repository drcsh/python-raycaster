import json
import os

from engine.config.config_data import Config


class ConfigLoader:
    """Static utility class for loading configuration from JSON files"""

    @staticmethod
    def load_config(config_file_path: str) -> Config:
        """
        Load configuration from JSON file and return Config object

        Args:
            config_file_path: Full path to config.json file

        Returns:
            Config: Initialized Config object

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If JSON is malformed
            ValueError: If config data is invalid
        """
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file not found: {config_file_path}")

        try:
            with open(config_file_path, 'r') as f:
                config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in config file {config_file_path}: {e.msg}",
                e.doc,
                e.pos
            )

        # Validate the loaded data
        ConfigLoader.validate_config_data(config_data)

        # Create and return Config object
        return Config(
            dev_mode=config_data.get('dev_mode', False),
            resolution_width=config_data['resolution']['width'],
            resolution_height=config_data['resolution']['height'],
            field_of_view=config_data.get('field_of_view', 60)
        )

    @staticmethod
    def validate_config_data(config_data: dict) -> bool:
        """
        Validate config data structure

        Args:
            config_data: Dict containing config data

        Returns:
            bool: True if valid

        Raises:
            ValueError: If config data is invalid
        """
        # Check required fields
        if 'resolution' not in config_data:
            raise ValueError("Missing required field: resolution")

        # Validate resolution structure
        resolution = config_data['resolution']
        if not isinstance(resolution, dict):
            raise ValueError("'resolution' must be a dict")

        required_resolution_fields = ['width', 'height']
        for field in required_resolution_fields:
            if field not in resolution:
                raise ValueError(f"Missing required resolution field: {field}")

            if not isinstance(resolution[field], int) or resolution[field] <= 0:
                raise ValueError(f"Resolution '{field}' must be a positive integer")

        # Validate field_of_view if present
        if 'field_of_view' in config_data:
            fov = config_data['field_of_view']
            if not isinstance(fov, int) or fov <= 0 or fov >= 180:
                raise ValueError("'field_of_view' must be an integer between 1 and 179")

        # Validate dev_mode if present
        if 'dev_mode' in config_data:
            if not isinstance(config_data['dev_mode'], bool):
                raise ValueError("'dev_mode' must be a boolean")

        return True
