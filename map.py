import pygame
import numpy as np
import math

PLAYER_WIDTH = 5
PLAYER_HEIGHT = 5
PLAYER_COLOR = (255, 255, 255)


class Map:

    default_squares_x = 16
    default_squares_y = 16

    def __init__(self, win_w, win_h, map_str, map_squares_x=default_squares_x, map_squares_y=default_squares_y):
        """
        Sets up a level Map with a grid coordinate system for locating objects easily, and an underlying pygame.Surface
        which will be used for more fine-grained tracking and for raycasting.

        :param win_w:
        :param win_h:
        :param map_str:
        :param map_squares_x:
        :param map_squares_y:
        """

        assert (len(map_str) == map_squares_x * map_squares_y)

        self.screen_width = win_w
        self.screen_height = win_h

        self.map_str = map_str
        self.map_squares_x = map_squares_x
        self.map_squares_y = map_squares_y

        # Each char in the map_str represents a rectangular area, which will have a certain size in pixels defined by
        # the surface x & y / map x & y
        # We will use these rectangles to divide up the map for locating things
        self.map_square_width = self.screen_width / (self.map_squares_x * 2)  # temp for split screen
        self.map_square_height = self.screen_height / self.map_squares_y

        self.surface = None
        self.reset_surface()

    def draw_map_to_surface(self, surface):
        """
        Given a surface, draws the map (defined in self.map_str) on top of it and returns the surface

        :param surface:
        :return:
        """
        # We will be drawing some pixels over the surface
        px_map = pygame.PixelArray(surface)

        for y in range(self.map_squares_y):
            for x in range(self.map_squares_x):
                if self.map_str[x + y * self.map_squares_x] == ' ':
                    continue  # skip empty spaces

                # Work out top left corner x, y and the bottom right x, y
                rect_tl_x = int(x * self.map_square_width)
                rect_tl_y = int(y * self.map_square_height)
                rect_br_x = int(rect_tl_x + self.map_square_width)
                rect_br_y = int(rect_tl_y + self.map_square_height)

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
        map_index = math.floor(x) + math.floor(y)*self.map_squares_x
        return self.map_str[map_index]

    def get_pixel_xy_from_map_xy(self, map_x, map_y):
        px_x = math.floor(map_x * self.map_square_width)
        px_y = math.floor(map_y * self.map_square_height)
        return px_x, px_y

    def draw_player(self, player_x, player_y):

        player_tl_x = math.floor(player_x * self.map_square_width)
        player_tl_y = math.floor(player_y * self.map_square_height)
        player_br_x = player_tl_x + PLAYER_WIDTH
        player_br_y = player_tl_y + PLAYER_HEIGHT

        px_map = pygame.PixelArray(self.surface)
        px_map[player_tl_x:player_br_x, player_tl_y:player_br_y] = PLAYER_COLOR

    def reset_surface(self):
        """
        Resets the surface to its initial state with the map on it.
        :return:
        """
        background = pygame.Surface((self.screen_width, self.screen_height))
        background.fill((255, 255, 255))
        self.surface = self.draw_map_to_surface(background)
