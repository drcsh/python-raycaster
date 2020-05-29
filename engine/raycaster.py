import math

from pygame import Rect

from engine.levelmapsurface import LevelMapSurface
from engine import math_utils


class RayCaster:

    DRAW_DISTANCE = 16

    def __init__(self, display_surface, game_map, fov, wall_textures, dev_mode=False):
        self.display_surface = display_surface
        self.current_map = game_map
        self.win_w = display_surface.get_width()
        self.win_h = display_surface.get_height()
        self.fov = fov
        self.wall_textures = wall_textures
        self.dev_mode = dev_mode
        
        # we will need these values multiple times
        self.half_fov = self.fov / 2
        self.half_win_h = self.win_h / 2
        self.half_win_w = self.win_w / 2

        self.map_surface = None
        if dev_mode:
            # In dev mode set up the map to appear on the left half of the screen
            map_rect = Rect((0, 0, self.half_win_w, self.win_h))
            map_surface_surface = self.display_surface.subsurface(map_rect)
            self.map_surface = LevelMapSurface(self.current_map, map_surface_surface)

    def cast(self, origin_x, origin_y, angle_from_x_axis):
        """
        Raycasts onto self.display_surface based on the location and angle given, and self.current_map

        :param float origin_x:
        :param float origin_y:
        :param float angle_from_x_axis:
        :return:
        """

        if self.dev_mode:
            self.map_surface.draw_map_to_surface()
            render_area_width = math.floor(self.half_win_w)
            px_x, px_y = self.map_surface.get_pixel_xy_from_map_xy(origin_x, origin_y)
            self.display_surface.set_at((px_x, px_y), (100, 255, 0))
        else:
            render_area_width = self.win_w

        # for every pixel in the window width
        for i in range(render_area_width):

            # pixel x on the screen we are going to render on this iteration, same as i except in dev mode
            screen_px_x = i

            # The angle of the ray is calculated around the center point which is where the player is facing
            angle = angle_from_x_axis - self.half_fov + (self.fov * i) / self.win_w

            if self.dev_mode:  # in dev mode we render the map on the left
                screen_px_x += render_area_width
                angle = angle_from_x_axis - self.half_fov + (self.fov * i) / (self.win_w / 2)

            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)

            ray_x = origin_x + 0.05 * cos_angle
            ray_y = origin_y + 0.05 * sin_angle

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
                x_increasing = ray_x > origin_x

                # y intercept
                intercept = origin_y - (gradient * origin_x)

            # check for horizontal lines
            if ray_y != origin_y:
                y_increasing = ray_y > origin_y

            # It's very unlikely that the first points we've chosen are whole, but they might be.
            ray_x_whole = ray_x % 1 == 0
            ray_y_whole = ray_y % 1 == 0

            counter = 0
            while counter < self.DRAW_DISTANCE:
                # Anything that happens in here will be called a *lot*.

                x_poi_x, x_poi_y = self.get_next_x_poi(origin_x, ray_x, gradient, intercept, x_increasing, ray_x_whole)
                y_poi_x, y_poi_y = self.get_next_y_poi(origin_x, origin_y, ray_y, gradient, intercept, y_increasing, ray_y_whole)
                ray_x, ray_y = math_utils.get_closest_point(ray_x, ray_y, x_poi_x, x_poi_y, y_poi_x, y_poi_y)

                # the ray will be one of the identified POIs, so one of the x/y values will be whole
                ray_x_whole = ray_x == x_poi_x
                ray_y_whole = ray_y == y_poi_y

                # draw visibility cone on map
                if self.dev_mode:
                    px_x, px_y = self.map_surface.get_pixel_xy_from_map_xy(ray_x, ray_y)
                    self.display_surface.set_at((px_x, px_y), (255, 100, 0))

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
                    ray_dist = math_utils.distance_formula(origin_x, origin_y, ray_x, ray_y)
                    column_height = math.floor(self.win_h / (ray_dist * math.cos(angle - angle_from_x_axis)))
                    column_start_y = math.floor(self.half_win_h - (column_height / 2))

                    # The ray's location when it stopped will be a map square with a fraction. E.g. 3.456
                    # If we home in on the fractional part of the value, we have a fraction which expresses how far
                    # along the map square we are. Since the wall texture tiles are mapped 1:1 with map squares, we
                    # can use this fraction to figure out the horizontal slice of the texture to get.
                    # However, when rendering a 'vertical' wall (top down perspective), x will be ~0, and y will be used
                    hit_x, _ = math.modf(ray_x)
                    hit_y, _ = math.modf(ray_y)
                    if math.fabs(hit_y) > math.fabs(hit_x):
                        hit_x_coord = hit_y * self.wall_textures.tile_size
                    else:
                        hit_x_coord = hit_x * self.wall_textures.tile_size

                    if hit_x_coord < 0:
                        hit_x_coord = math.fabs(hit_x_coord)

                    tile_slice = self.wall_textures.get_tile_slice(int(map_symbol), 0, int(hit_x_coord), column_height)

                    self.display_surface.blit(tile_slice, (screen_px_x, column_start_y))

                    break
                counter += 1

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
            if x_whole:
                next_whole_x = ray_x + 1
            else:
                next_whole_x = math.ceil(ray_x)

        else:
            if x_whole:
                next_whole_x = ray_x - 1
            else:
                next_whole_x = math.floor(ray_x)

        y_at_next_whole_x = math_utils.get_y_for_x(next_whole_x, gradient, intercept)

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
            if y_whole:
                next_whole_y = ray_y + 1
            else:
                next_whole_y = math.ceil(ray_y)

        else:
            if y_whole:
                next_whole_y = ray_y - 1
            else:
                next_whole_y = math.floor(ray_y)

        if gradient:
            x_at_next_whole_y = math_utils.get_x_for_y(next_whole_y, gradient, intercept)
        else:  # vertical line, y changes but x is the same as origin
            x_at_next_whole_y = origin_x

        return x_at_next_whole_y, next_whole_y