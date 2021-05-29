import math

import pygame

from engine.level_objects.levelmap import LevelMap


class LevelMapSurface:
    """
    This is a hybrid class which relates a LevelMap to a Surface, allowing for easily drawing the map and translating
    between map coordinates and pixels on the surface. This is presently only used for debug mode, but could be
    turned into a map for the player_objects.
    """

    def __init__(self, level_map: LevelMap, surface: pygame.Surface):
        """
        :param LevelMap level_map:
        :param Surface surface: Surface to draw the map onto
        """
        self.level_map = level_map
        self.surface = surface

        self.map_square_px_width = self.surface.get_width() / self.level_map.map_squares_x
        self.map_square_px_height = self.surface.get_height() / self.level_map.map_squares_y

    def get_pixel_xy_from_map_xy(self, map_x: float, map_y: float):
        """
        Translates a map coordinate to a pixel.

        :param float map_x:
        :param float map_y:
        :return:
        """
        px_x = math.floor(map_x * self.map_square_px_width)
        px_y = math.floor(map_y * self.map_square_px_height)
        return px_x, px_y

    def draw_map_to_surface(self):
        """
        Draws the game map onto self.surface
        """
        # We will be drawing some pixels over the surface
        px_map = pygame.PixelArray(self.surface)

        for y in range(self.level_map.map_squares_y):
            for x in range(self.level_map.map_squares_x):
                if self.level_map.map_str[x + y * self.level_map.map_squares_x] == ' ':
                    continue  # skip empty spaces

                # Work out top left corner x, y and the bottom right x, y
                rect_tl_x = int(x * self.map_square_px_width)
                rect_tl_y = int(y * self.map_square_px_height)
                rect_br_x = int(rect_tl_x + self.map_square_px_width)
                rect_br_y = int(rect_tl_y + self.map_square_px_height)

                # Draws a rectangle from x1:x2 and y1:y2
                px_map[rect_tl_x:rect_br_x, rect_tl_y:rect_br_y] = (0, 255, 255)

        px_map.close()
