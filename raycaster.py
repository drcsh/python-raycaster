import math
import numpy as np
from pygame import PixelArray

from map import Map


class RayCaster:

    def __init__(self, win_w, win_h, fov):
        self.win_w = win_w
        self.win_h = win_h
        self.fov = fov

    def cast(self, game_map, origin_x, origin_y, player_angle):
        """

        :param Map game_map:
        :param float origin_x:
        :param float origin_y:
        :param float player_angle:
        :return:
        """

        px_map = PixelArray(game_map.surface)

        # for every pixel in the window width
        for i in range(self.win_w):

            # get the angle of this ray, calculated around the center point which is where the player is facing
            angle = player_angle - self.fov / 2 + self.fov * i / self.win_w

            # draw a ray from the origin until we hit an obstacle on the game map
            for t in np.arange(0, 20, 0.05):
                ray_x = origin_x + t * math.cos(angle)
                ray_y = origin_y + t * math.sin(angle)

                # print(ray_x, ray_y)

                map_symbol = game_map.get_symbol_at_map_xy(ray_x, ray_y)

                # hit a wall
                if map_symbol != " ":
                    break

                px_x, px_y = game_map.get_pixel_xy_from_map_xy(ray_x, ray_y)

                px_map[px_x, px_y] = (255, 255, 255)

        px_map.close()
