import math
import random

from map import Map


class RayCaster:

    DRAW_DISTANCE = 16

    def __init__(self, win_w, win_h, fov, wall_textures):
        self.win_w = win_w
        self.win_h = win_h
        self.fov = fov
        self.half_fov = self.fov / 2
        self.wall_textures = wall_textures

        self.current_map = None

        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(10)]

    def cast(self, game_map, origin_x, origin_y, player_angle):
        """

        :param Map game_map:
        :param float origin_x:
        :param float origin_y:
        :param float player_angle:
        :return:
        """
        self.current_map = game_map
        render_area_start_x = math.floor(self.win_w / 2)

        px_x, px_y = self.current_map.get_pixel_xy_from_map_xy(origin_x, origin_y)
        self.current_map.surface.set_at((px_x, px_y), (100, 255, 0))

        # for every pixel in the window width
        for i in range(render_area_start_x):  # draw the visibility cone AND the "3D" view

            # pixel x we are going to render on this iteration
            px = render_area_start_x + i

            # get the angle of this ray, calculated around the center point which is where the player is facing
            angle = player_angle - self.half_fov + (self.fov * i) / (self.win_w / 2)
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)

            ray_x = origin_x + 0.1 * cos_angle
            ray_y = origin_y + 0.1 * sin_angle

            px_x, px_y = self.current_map.get_pixel_xy_from_map_xy(ray_x, ray_y)
            self.current_map.surface.set_at((px_x, px_y), (100, 255, 0))

            # what I want to do is calculate the next point(s) of interest (POI) on the graph, which are where the ray
            # would cross into another map square. To do this, I need to figure out the direction of travel of the ray,
            # e.g. weather we are going up/down the x and y axis
            # I also need to solve the linear equation for the ray. With this info, we can calculate
            # where the ray will cross into the next map squares (i.e. hit the next whole x and whole y numbers).
            # with those coordinates known, we figure out which is closest and whether or not we hit a wall, then
            # keep figuring out the next POI until we do hit a wall or we hit the draw distance

            x_increasing = False
            y_increasing = False

            intercept = None  # y intercept, if this line is not vertical
            gradient = None  # gradient of this line

            # Work out the gradient + intercept (as long as not a vertical line) and whether the x and y values
            # are increasing relative to the player
            if ray_x != origin_x:
                gradient = (ray_y - origin_y) / (ray_x - origin_x)
                if ray_x > origin_x:
                    x_increasing = True

                # y intercept
                intercept = origin_y - (gradient * origin_x)

            if ray_y != origin_y:  # as long as it's not horizontal
                if ray_y > origin_y:
                    y_increasing = True

            ray_x_whole = ray_x % 1 == 0
            ray_y_whole = ray_y % 1 == 0

            counter = 0
            while counter < self.DRAW_DISTANCE:
                counter += 1

                poi_x = self.get_next_x_poi(origin_x, ray_x, gradient, intercept, x_increasing, ray_x_whole)
                poi_y = self.get_next_y_poi(origin_x, origin_y, ray_y, gradient, intercept, y_increasing, ray_y_whole)
                ray_x, ray_y = self.get_closest_poi((ray_x, ray_y), poi_x, poi_y)

                ray_x_whole = ray_x % 1 == 0
                ray_y_whole = ray_y % 1 == 0

                # get pixel location on map
                px_x, px_y = self.current_map.get_pixel_xy_from_map_xy(ray_x, ray_y)

                # draw visibility cone on map
                self.current_map.surface.set_at((px_x, px_y), (255, 100, 0))

                # If the Ray is at a whole number on the x/y grid, and is decreasing on that axis, the next wall it hits
                # will actually be in the map square 1 over from the ray. I.e. if we're at square 2,1 and looking
                # leftwards on the map, we need to render the wall at 1,1, not the lack of wall at 2,1.
                plot_x = ray_x
                plot_y = ray_y
                if ray_x_whole and not x_increasing:
                    plot_x = ray_x - 1

                if ray_y_whole and not y_increasing:
                    plot_y = ray_y - 1

                map_symbol = self.current_map.get_symbol_at_map_xy(plot_x, plot_y)

                # hit a wall
                if map_symbol != " ":
                    # if we're looking straight at the wall, the col_h is the win_h / distance. To correct fisheye
                    # distortion we get the angle of the current col away from the centre line of the player's vision
                    # (angle - the player angle). cos of that angle is a proportion of the height if we were looking
                    # straight at it.
                    ray_dist = self.distance_formula((origin_x, origin_y), (ray_x, ray_y))
                    column_height = math.floor(self.win_h / (ray_dist * math.cos(angle - player_angle)))
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

                    tile_slice = self.wall_textures.get_tile_slice(int(map_symbol), 0, int(hit_x_coord), column_height)

                    self.current_map.surface.blit(tile_slice, (px, column_start_y))

                    break

    def get_next_x_poi(self, origin_x, ray_x, gradient, intercept, x_increasing, x_whole):
        """
        Finds the next x Point of Interest on this line. I.e. the coordinate where the ray defined by the parameters
        will be a whole x value.

        e.g. If the current ray is at x=1, y=1.5 and we know that x is increasing, the next whole x will be 2, and we
        will need to user the gradient and intercept to calculate y at this location.

        If the line is vertical (i.e. x doesn't change) then there will not be another x POI.

        :param float origin_x:
        :param float ray_x:
        :param float gradient:
        :param float intercept:
        :param bool x_increasing:
        :param bool x_whole:
        :return:
        :rtype tuple: (float, float) or (None, None)
        """


        if ray_x == origin_x:  # vertical line. Y varies but not x
            return None, None

        if x_increasing:
            if ray_x < self.current_map.map_squares_x:
                if x_whole:
                    next_whole_x = ray_x + 1
                else:
                    next_whole_x = math.ceil(ray_x)
            else:
                next_whole_x = self.current_map.map_squares_x
        else:
            if ray_x > 0:
                if x_whole:
                    next_whole_x = ray_x - 1
                else:
                    next_whole_x = math.floor(ray_x)
            else:
                next_whole_x = 0

        y_at_next_whole_x = self.get_y_for_x(next_whole_x, gradient, intercept)

        return next_whole_x, y_at_next_whole_x

    def get_next_y_poi(self, origin_x, origin_y, ray_y, gradient, intercept, y_increasing, y_whole):
        """
        Finds the next y Point of Interest on this line. I.e. the coordinate where the ray defined by the parameters
        will be a whole y value.

        Works similarly to the next_x poi, but if the line is horizontal (i.e. y doesn't change) there will be no next
        y POI.

        This requires an additional parameter to next_x_poi, because in the case that the line is vertical, there will
        be a next y poi, but we won't have a gradient or intercept because the line is vertical, so we need the origin_x
        to set the x value.

        :param float origin_x:
        :param float origin_y:
        :param float ray_y:
        :param float gradient:
        :param float intercept:
        :param bool y_increasing:
        :param bool y_whole:
        :return: coordinate
        :rtype tuple: (float, float) or (None, None)
        """

        if ray_y == origin_y:  # horizontal line. x varies but not y
            return None, None

        if y_increasing:
            if ray_y < self.current_map.map_squares_y:
                if y_whole:
                    next_whole_y = ray_y + 1
                else:
                    next_whole_y = math.ceil(ray_y)
            else:
                next_whole_y = ray_y

        else:
            if ray_y > 0:
                if y_whole:
                    next_whole_y = ray_y - 1
                else:
                    next_whole_y = math.floor(ray_y)
            else:
                next_whole_y = 0

        if gradient and intercept:
            x_at_next_whole_y = self.get_x_for_y(next_whole_y, gradient, intercept)
        else:  # vertical line, y changes but x is the same as origin
            x_at_next_whole_y = origin_x

        return x_at_next_whole_y, next_whole_y

    def distance_formula(self, point_1, point_2):
        """
        Distance between two points is defined as the square root of (x2 - x1)^2 + (y2 - y1) ^ 2

        :param tuple(float, float) point_1:
        :param tuple(float, float) point_2:
        :return: distance
        :rtype float:
        """
        x1 = point_1[0]
        y1 = point_1[1]

        x2 = point_2[0]
        y2 = point_2[1]

        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    def get_y_for_x(self, x, gradient, y_intercept):
        """
        Linear equation, y = mx + c

        :param float x:
        :param float gradient:
        :param float y_intercept:
        :return:
        """
        return (x * gradient) + y_intercept

    def get_x_for_y(self, y, gradient, y_intercept):
        """
        Linear equation reorganised, x = (y - c) / m
        :param float y:
        :param float gradient:
        :param float y_intercept:
        :return:
        """
        return (y - y_intercept) / gradient

    def get_closest_poi(self, current_coord, poi_1, poi_2):
        """
        Given a current position and two other positions which we're interested in, works out which of the two is
        closest to the current position

        :param tuple(float, float) current_coord:
        :param tuple(float, float) poi_1: Coordinate of a POI. May be partial (e.g. either value None)
        :param tuple(float, float) poi_2: Coordinate of a POI. May be partial (e.g. either value None)
        :return: the closest point to the current one
        :rtype tuple(float, float):
        """

        # if we found two potential points of interest, which is closer to the origin?
        if poi_1[0] and poi_1[1] and poi_2[0] and poi_2[1]:
            dist_1 = self.distance_formula(current_coord, poi_1)
            dist_2 = self.distance_formula(current_coord, poi_2)

            if dist_1 < dist_2:
                return poi_1
            else:
                return poi_2

        # else we only have 1 point to chose from anyway...
        elif poi_1[0] and poi_1[1]:
            return poi_1

        else:
            return poi_2
