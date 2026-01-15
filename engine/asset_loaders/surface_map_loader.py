import os

import pygame

from engine.surfaces.surface_map import SurfaceMap

#Todo: move this to a config file?
TEXTURES_BASE_PATH = os.path.join('assets', 'textures')

class SurfaceMapLoader:
    """Static utility class for loading surface maps from texture files"""

    

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
        full_path = os.path.join(TEXTURES_BASE_PATH, file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Texture file not found: {full_path}")

        surface = pygame.image.load(full_path)
        return SurfaceMap(surface)
