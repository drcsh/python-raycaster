import pygame

from engine.textures.texturemap import TextureMap
from engine.textures.texturetile import TextureTile


class GameObject(pygame.sprite.Sprite):
    """
    For keeping track of anything which appears within the level and is rendered as an object in the world. I.e.
    not the walls and floor.

    This class by itself can render static furniture.
    Parent for AnimatedObject which covers enemies etc.
    """

    def __init__(self, sprite_group: pygame.sprite.Group, x: float, y: float, texturemap: TextureMap):
        """
        :param sprite_group: SpriteGroup for keeping track of this object
        :param x: X Coord on the map
        :param y: Y Coord on the map
        :param texturemap: TextureMap to render.
        """
        self.x = x
        self.y = y
        self.texturemap = texturemap
        super(GameObject, self).__init__(sprite_group)

    def get_display_tile(self) -> TextureTile:
        """
        Returns the tile from the texturemap for display.

        This is here so that in RayCaster we can treat static game furniture and animated objects the same way
        for rendering purposes.
        """
        return self.texturemap.get_tile_at(0, 0)
