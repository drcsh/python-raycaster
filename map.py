from pygame import PixelArray
import numpy as np
import math

PLAYER_WIDTH = 5
PLAYER_HEIGHT = 5
PLAYER_COLOR = (255, 255, 255)


class Map:
    """
    :TODO: clear up the distinction between map coordinates and pixel coordinates
    """

    default_width = 16
    default_height = 16

    def __init__(self, surface, map_str, width=default_width, height=default_height):
        """
        Given a surface to use at the background to the image, and a map_str, draws features onto the surface to use as
        the game map.

        Presently only draws walls (any non space character) or nothing (space)

        :param surface:
        :param map_str:
        :param width:
        :param height:
        """
        assert (len(map_str) == width * height)

        self.map_str = map_str
        self.width = width
        self.height = height

        # Each char in the map_str represents a rectangular area, which will have a certain size in pixels defined by
        # the surface x & y / map x & y
        # We will use these rectangles to divide up the map for locating things
        self.rect_width = surface.get_width() / self.width
        self.rect_height = surface.get_width() / self.height

        self.surface = self.draw_map_to_surface(surface)

    def draw_map_to_surface(self, surface):
        """
        Given a surface, draws the map (defined in self.map_str) on top of it and returns the surface

        :param surface:
        :return:
        """
        # We will be drawing some pixels over the surface
        px_map = PixelArray(surface)

        for y in range(self.height):
            for x in range(self.width):
                if self.map_str[x + y * self.width] == ' ':
                    continue  # skip empty spaces

                # Work out top left corner x, y and the bottom right x, y
                rect_tl_x = int(x * self.rect_width)
                rect_tl_y = int(y * self.rect_height)
                rect_br_x = int(rect_tl_x + self.rect_width)
                rect_br_y = int(rect_tl_y + self.rect_height)

                # Draws a rectangle from x1:x2 and y1:y2
                px_map[rect_tl_x:rect_br_x, rect_tl_y:rect_br_y] = (0, 255, 255)

        px_map.close()
        return surface

    def get_symbol_at_map_xy(self, x, y):
        """
        Get the map symbol at the map coordinate
        :param x:
        :param y:
        :return:
        """
        map_index = math.floor(x) + math.floor(y)*self.width
        return self.map_str[map_index]

    def get_pixel_xy_from_map_xy(self, map_x, map_y):
        px_x = math.floor(map_x * self.rect_width)
        px_y = math.floor(map_y * self.rect_height)
        return px_x, px_y

    def draw_player(self, player_x, player_y):

        player_tl_x = math.floor(player_x * self.rect_width)
        player_tl_y = math.floor(player_y * self.rect_height)
        player_br_x = player_tl_x + PLAYER_WIDTH
        player_br_y = player_tl_y + PLAYER_HEIGHT

        px_map = PixelArray(self.surface)
        px_map[player_tl_x:player_br_x, player_tl_y:player_br_y] = PLAYER_COLOR

    def ray_cast(self, origin_x, origin_y, angle):

        px_map = PixelArray(self.surface)

        for c in np.arange(0, 20, 0.05):
            ray_x = origin_x + c * math.cos(angle)
            ray_y = origin_y + c * math.sin(angle)

            #print(ray_x, ray_y)

            map_symbol = self.get_symbol_at_map_xy(ray_x, ray_y)

            # hit a wall
            if map_symbol != " ":
                break

            px_x, px_y = self.get_pixel_xy_from_map_xy(ray_x, ray_y)

            px_map[px_x:px_x+2, px_y:px_y+2] = (255, 255, 255)

        px_map.close()
