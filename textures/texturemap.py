import math
import pygame


class TextureLookupException(BaseException):
    pass


class TextureMap:
    DEFAULT_TEXTURE_TILE_SIZE = 64

    @staticmethod
    def load_from_file(filename):
        surface = pygame.image.load(filename)
        return TextureMap(surface)

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
                subsurface = self.surface.subsurface(tile_rect)
                tile = TextureTile(subsurface)
                self._tiles.append(tile)

    def get_tile_at(self, x, y):
        """
        Get the TextureTile at the given x/y coordinate.

        :param int x:
        :param int y:
        :return:
        :rtype TextureTile:
        :raises TextureLookupException: if the tile coord is invalid.
        """
        if x < 0 or x > self.total_hrz_tiles:
            raise TextureLookupException(f"X coord '{x}' out of range")
        if y < 0 or y > self.total_vrt_tiles:
            raise TextureLookupException(f"Y coord '{y}' out of range")

        return self._tiles[x+y*self.total_vrt_tiles]

    def get_tile_slice(self, tile_x, tile_y, tile_slice_at_x, scale_to_h):
        """
        Fetches the texture tile at location tile_x/tile_y and creates a 1px wide slice of it at the given x value
        within that tile.

        :param int tile_x: The tile x loc on the texture
        :param int tile_y: The tile y loc on the texture
        :param int tile_slice_at_x: the pixel location on the tile to slice at.
        :param int scale_to_h: the height to scale the slice to (will take a full vert-slice and scale to this size)
        :return:
        """
        # fetch the tile
        tile = self.get_tile_at(tile_x, tile_y)

        tile_slice = tile.get_slice_at_x(tile_slice_at_x)

        # do the scaling
        tile_slice = pygame.transform.smoothscale(tile_slice, (1, scale_to_h))

        return tile_slice


class TextureTile:

    def __init__(self, surface):
        self.surface = surface
        self._slices = self._generate_slice_array()

    def _generate_slice_array(self):
        """
        Creates an array of 1 pixel wide slices of this tile needed for raycasting.

        :return: slices - list of subsurfaces of self.surface
        :rtype: list
        """
        slices = []
        for x in range(self.surface.get_width()):
            slice_rect = pygame.Rect(x, 0, 1, self.surface.get_width())
            slices.append(self.surface.subsurface(slice_rect))
        return slices

    def get_slice_at_x(self, x):
        return self._slices[x]
