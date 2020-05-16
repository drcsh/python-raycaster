import math
import numpy as np
import random
from pygame import PixelArray

from map import Map
from timeit import default_timer as timer

class RayCaster:

    def __init__(self, win_w, win_h, fov):
        self.win_w = win_w
        self.win_h = win_h
        self.fov = fov
        self.half_fov = self.fov / 2

        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(10)]

    def cast(self, game_map, origin_x, origin_y, player_angle):
        """

        :param Map game_map:
        :param float origin_x:
        :param float origin_y:
        :param float player_angle:
        :return:
        """
        render_area_start_x = math.floor(self.win_w / 2)
        px_map = PixelArray(game_map.surface)

        # for every pixel in the window width
        for i in range(render_area_start_x):  # draw the visibility cone AND the "3D" view
            # pixel x we are going to render on this iteration
            px = render_area_start_x + i

            # get the angle of this ray, calculated around the center point which is where the player is facing
            angle = player_angle - self.half_fov + (self.fov * i) / (self.win_w / 2)

            # draw a ray from the origin until we hit an obstacle on the game map
            for t in np.arange(0, 20, 0.05):
                ray_x = origin_x + t * math.cos(angle)
                ray_y = origin_y + t * math.sin(angle)

                # print(ray_x, ray_y)

                map_symbol = game_map.get_symbol_at_map_xy(ray_x, ray_y)

                # hit a wall
                if map_symbol != " ":
                    column_height = self.win_h / t  # height of the wall is inversely proportional to dist from player
                    column_start_y = math.floor((self.win_h/2) - (column_height / 2))
                    col_end_y = math.floor(column_start_y + column_height)

                    px_map[px, column_start_y:col_end_y] = self.colors[int(map_symbol)]
                    break

                px_x, px_y = game_map.get_pixel_xy_from_map_xy(ray_x, ray_y)

                px_map[px_x, px_y] = (255, 255, 0)

        px_map.close()
