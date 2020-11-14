import pygame


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

    def get_scaled_slice_at_x(self, x, scale_to_h):
        """
        Get a vertical slice of this tile at pix loc x, and scale it to a desired height.

        :param int x: the pixel location on the tile to slice at.
        :param int scale_to_h: the height to scale the slice to (will take a full vert-slice and scale to this size)
        :return:
        """
        tile_slice = self.get_slice_at_x(x)

        tile_slice = pygame.transform.smoothscale(tile_slice, (1, scale_to_h))

        return tile_slice