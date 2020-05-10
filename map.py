from pygame import PixelArray
import math

PLAYER_WIDTH = 5
PLAYER_HEIGHT = 5
PLAYER_COLOR = (255, 255, 255)


class Map:

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

        # We will be drawing some pixels over the surface
        px_map = PixelArray(surface)

        # Each char in the map_str represents a rectangular area, which will have a certain size in pixels defined by
        # the surface x & y / map x & y
        # We will use these rectangles to divide up the map for locating things
        self.rect_width = surface.get_width() / width
        self.rect_height = surface.get_width() / height

        for y in range(height):
            for x in range(width):
                if map_str[x + y * width] == ' ':
                    continue  # skip empty spaces

                # Work out top left corner x, y and the bottom right x, y
                rect_tl_x = int(x * self.rect_width)
                rect_tl_y = int(y * self.rect_height)
                rect_br_x = int(rect_tl_x + self.rect_width)
                rect_br_y = int(rect_tl_y + self.rect_height)

                # Draws a rectangle from x1:x2 and y1:y2
                px_map[rect_tl_x:rect_br_x, rect_tl_y:rect_br_y] = (0, 255, 255)

        px_map.close()

        self.surface = surface

    def draw_player(self, player_x, player_y):

        player_tl_x = math.floor(player_x * self.rect_width)
        player_tl_y = math.floor(player_y * self.rect_height)
        player_br_x = player_tl_x + PLAYER_WIDTH
        player_br_y = player_tl_y + PLAYER_HEIGHT

        px_map = PixelArray(self.surface)
        px_map[player_tl_x:player_br_x, player_tl_y:player_br_y] = PLAYER_COLOR
