import math
import pygame


class TextureLookupException(BaseException):
    pass


class TextureLoader:

    @staticmethod
    def get_texture(filename):
        surface = pygame.image.load(filename)
        return Texture(surface)


class Texture:
    DEFAULT_TEXTURE_TILE_SIZE = 64

    def __init__(self, surface, tile_size=DEFAULT_TEXTURE_TILE_SIZE):
        """
        Given a surface and a (optional) tilesize, splits up the surface into subsurfaces (tiles) of w/h tile_size.

        :param pygame.Surface surface:
        :param int tile_size:
        :raises IOError: can't divide surface by tile size to get a round number of tiles.
        """

        if surface.get_width() % tile_size != 0 or surface.get_height() % tile_size != 0:
            raise IOError("Texture initialized with surface which is not divisible by the tile size. This means that "
                          "the texture cannot be split into tiles!")

        self.surface = surface
        self.tile_size = tile_size
        self.total_hrz_tiles = math.floor(self.surface.get_width() / tile_size)
        self.total_vrt_tiles = math.floor(self.surface.get_height() / tile_size)

        # This will be a 2d array packed into a 1d one
        self._tiles = []
        for vert in range(self.total_vrt_tiles):
            for hrz in range(self.total_hrz_tiles):
                tile_rect = pygame.Rect(hrz * self.tile_size, vert * self.tile_size, self.tile_size, self.tile_size)

                self._tiles.append(self.surface.subsurface(tile_rect))

    def get_tile_at(self, x, y):
        """
        Get the texture tile at the given x/y coordinate.

        :param int x:
        :param int y:
        :return:
        :rtype pygame.Surface:
        :raises TextureLookupException: if the tile coord is invalid.
        """
        if x < 0 or x > self.total_hrz_tiles:
            raise TextureLookupException(f"X coord '{x}' out of range")
        if y < 0 or y > self.total_vrt_tiles:
            raise TextureLookupException(f"Y coord '{y}' out of range")

        return self._tiles[x+y*self.total_vrt_tiles]

    def get_tile_slice(self, tile_x, tile_y, tile_slice_at_x, slice_w, scale_to_h):
        """
        Fetches the texture tile at location tile_x/tile_y and creates a vertical slice of it.

        :param int tile_x: The tile x loc on the texture
        :param int tile_y: The tile y loc on the texture
        :param int tile_slice_at_x: the pixel location to slice at.
        :param int slice_w: the width of the slice
        :param int scale_to_h: the height to scale the slice to (will take a full vert-slice and scale to this size)
        :return:
        """

        # fetch the tile
        tile = self.get_tile_at(tile_x, tile_y).copy()

        # get a vertical slice of the tile from hit_x, 0 at the top left, as wide as slice_w
        slice_rect = pygame.Rect(tile_slice_at_x, 0, slice_w, tile.get_height())
        tile_slice = tile.subsurface(slice_rect).copy()  # very important we take a copy, not the original

        # do the scaling
        tile_slice = pygame.transform.smoothscale(tile_slice, (slice_w, scale_to_h))

        return tile_slice

