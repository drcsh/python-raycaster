import os

import pygame

from engine.surfaces.surface_map import SurfaceMap


class SurfaceMapLoader:
    """Static utility class for loading surface maps from texture files"""

    TEXTURES_BASE_PATH = os.path.join('assets', 'textures')

    @staticmethod
    def load_surface_map(file_path: str) -> SurfaceMap:
        """
        Load a SurfaceMap from a file path

        Args:
            file_path: Path to the texture file (absolute or relative to project root)

        Returns:
            SurfaceMap: Loaded surface map

        Raises:
            FileNotFoundError: If texture file doesn't exist
            pygame.error: If file cannot be loaded as an image
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Texture file not found: {file_path}")

        surface = pygame.image.load(file_path)
        return SurfaceMap(surface)

    @staticmethod
    def load_texture(category: str, filename: str) -> SurfaceMap:
        """
        Load texture from assets/textures/{category}/{filename}

        Args:
            category: Subdirectory within textures (e.g., 'enemies', 'common')
            filename: Name of the texture file

        Returns:
            SurfaceMap: Loaded surface map
        """
        path = os.path.join(SurfaceMapLoader.TEXTURES_BASE_PATH, category, filename)
        return SurfaceMapLoader.load_surface_map(path)

    @staticmethod
    def load_enemy(filename: str) -> SurfaceMap:
        """
        Load enemy texture from assets/textures/enemies/

        Args:
            filename: Name of the enemy texture file

        Returns:
            SurfaceMap: Loaded surface map
        """
        return SurfaceMapLoader.load_texture('enemies', filename)

    @staticmethod
    def load_common(filename: str) -> SurfaceMap:
        """
        Load common texture from assets/textures/common/

        Args:
            filename: Name of the common texture file

        Returns:
            SurfaceMap: Loaded surface map
        """
        return SurfaceMapLoader.load_texture('common', filename)

    @staticmethod
    def load_wall_texture(filename: str) -> SurfaceMap:
        """
        Load wall texture from assets/textures/

        Args:
            filename: Name of the wall texture file

        Returns:
            SurfaceMap: Loaded surface map
        """
        path = os.path.join(SurfaceMapLoader.TEXTURES_BASE_PATH, filename)
        return SurfaceMapLoader.load_surface_map(path)
