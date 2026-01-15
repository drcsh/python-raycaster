import json
import os
from typing import List

import pygame

from engine.level_objects.level import Level
from engine.level_objects.levelmap import LevelMap
from engine.entities.enemy import Enemy
from engine.asset_loaders.surface_map_loader import SurfaceMapLoader


class LevelLoader:
    """Static utility class for loading levels from JSON files"""

    @staticmethod
    def load_level_data_from_file(level_file_path: str) -> dict:
        """
        Load and parse a level JSON file, return level data dict

        Args:
            level_file_path: Path to the level JSON file (absolute or relative to project root)

        Returns:
            dict: Parsed level data

        Raises:
            FileNotFoundError: If level file doesn't exist
            json.JSONDecodeError: If JSON is malformed
            ValueError: If level data is invalid
        """
        if not os.path.exists(level_file_path):
            raise FileNotFoundError(f"Level file not found: {level_file_path}")

        try:
            with open(level_file_path, 'r') as f:
                level_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in level file {level_file_path}: {e.msg}",
                e.doc,
                e.pos
            )

        # Validate the loaded data
        LevelLoader.validate_level_data(level_data)

        return level_data

    @staticmethod
    def validate_level_data(level_data: dict) -> bool:
        """
        Validate level data structure and contents

        Args:
            level_data: Dict containing level data

        Returns:
            bool: True if valid

        Raises:
            ValueError: If level data is invalid
        """
        # Check required fields
        required_fields = ['level_id', 'name', 'map', 'player_spawn', 'enemies']
        for field in required_fields:
            if field not in level_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate map structure
        map_data = level_data['map']
        required_map_fields = ['wall_texture','width', 'height', 'data']
        for field in required_map_fields:
            if field not in map_data:
                raise ValueError(f"Missing required map field: {field}")

        # Validate map dimensions
        width = map_data['width']
        height = map_data['height']
        map_str = map_data['data']

        expected_length = width * height
        actual_length = len(map_str)

        if actual_length != expected_length:
            raise ValueError(
                f"Map data length mismatch: expected {expected_length} "
                f"(width={width} × height={height}), got {actual_length}"
            )

        # Validate player spawn
        spawn = level_data['player_spawn']
        required_spawn_fields = ['x', 'y', 'angle']
        for field in required_spawn_fields:
            if field not in spawn:
                raise ValueError(f"Missing required player_spawn field: {field}")

        # Validate enemies array
        if not isinstance(level_data['enemies'], list):
            raise ValueError("'enemies' must be a list")

        # Validate each enemy
        for i, enemy in enumerate(level_data['enemies']):
            required_enemy_fields = ['x', 'y', 'texture_filename']
            for field in required_enemy_fields:
                if field not in enemy:
                    raise ValueError(f"Enemy {i}: missing required field '{field}'")

        return True

    @staticmethod
    def create_level_from_data(level_data: dict) -> Level:
        """
        Create a Level object from parsed JSON data

        Args:
            level_data: Dict containing level data from JSON

        Returns:
            Level: Initialized Level object
        """
        # Extract map data
        map_info = level_data['map']
        map_str = map_info['data']
        map_width = map_info.get('width', 16)
        map_height = map_info.get('height', 16)
        wall_texture_filename = map_info.get('wall_texture', 'walls.png')
        wall_surface_map = SurfaceMapLoader.load_surface_map(wall_texture_filename)

        # Create LevelMap
        level_map = LevelMap(map_str, map_width, map_height)

        # Initialize sprite groups
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        # Create enemies
        enemies_data = level_data.get('enemies', [])
        for enemy_dict in enemies_data:
            # Load enemy texture
            enemy_surface_map = SurfaceMapLoader.load_surface_map(enemy_dict['texture_filename'])

            # Get enemy parameters with defaults
            max_hp = enemy_dict.get('max_hp', 50)
            speed = enemy_dict.get('speed', 0.25)
            attack_range = enemy_dict.get('attack_range', 1.0)
            attack_damage = enemy_dict.get('attack_damage', 20)

            # Create enemy (auto-registers with sprite group)
            Enemy(
                sprite_group=enemies,
                x=enemy_dict['x'],
                y=enemy_dict['y'],
                surface_map=enemy_surface_map,
                max_hp=max_hp,
                speed=speed,
                attack_range=attack_range,
                attack_damage=attack_damage
            )

        # Create and return Level
        return Level(level_map, wall_surface_map, enemies, bullets)
