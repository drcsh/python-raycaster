import math
import numpy as np
import random

from map import Map


class RayCaster:

    def __init__(self, win_w, win_h, fov, wall_textures):
        self.win_w = win_w
        self.win_h = win_h
        self.fov = fov
        self.half_fov = self.fov / 2
        self.wall_textures = wall_textures

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
        #px_map = PixelArray(game_map.surface)

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

                # get pixel location on map
                px_x, px_y = game_map.get_pixel_xy_from_map_xy(ray_x, ray_y)

                # draw visibility cone on map
                game_map.surface.set_at((px_x, px_y), (255, 255, 0))

                # print(ray_x, ray_y)

                map_symbol = game_map.get_symbol_at_map_xy(ray_x, ray_y)

                # hit a wall
                if map_symbol != " ":
                    # if we're looking straight at the wall, the col_h is the win_h / distance. To correct fisheye
                    # distortion we get the angle of the current col away from the centre line of the player's vision
                    # (angle - the player angle). cos of that angle is a proportion of the height if we were looking
                    # straight at it.
                    column_height = math.floor(self.win_h / (t * math.cos(angle - player_angle)))
                    column_start_y = math.floor((self.win_h/2) - (column_height / 2))

                    # The ray's location when it stopped will be a map square with a fraction. E.g. 3.456
                    # If we home in on the fractional part of the value, we have a fraction which expresses how far
                    # along the map square we are. Since the wall texture tiles are mapped 1:1 with map squares, we
                    # can use this fraction to figure out the horizontal slice of the texture to get.
                    # However, when rendering a 'vertical' wall (top down perspective), x will be ~0, and y will be used
                    hit_x = ray_x - math.floor(ray_x+0.5)
                    hit_y = ray_y - math.floor(ray_y+0.5)
                    if math.fabs(hit_y) > math.fabs(hit_x):
                        hit_x_coord = hit_y * self.wall_textures.tile_size
                    else:
                        hit_x_coord = hit_x * self.wall_textures.tile_size

                    if hit_x_coord < 0:
                        hit_x_coord += self.wall_textures.tile_size

                    tile_slice = self.wall_textures.get_tile_slice(int(map_symbol), 0, hit_x_coord, 1, column_height)

                    game_map.surface.blit(tile_slice, (px, column_start_y))

                    break




