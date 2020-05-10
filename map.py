from pygame import PixelArray


class Map:

    default_width = 16
    default_height = 16

    @staticmethod
    def draw_on_surface(surface, map_str, width=default_width, height=default_height):
        """
        Given a surface to use at the background to the image, and a map_str, draws features onto the surface.
        Presently only draws walls (any non space character) or nothing (space)

        :param pygame.Surface surface:
        :param str map_str:
        :param int width: (optional)
        :param int height: (optional)
        :return:
        """
        assert(len(map_str) == width * height)

        # We will be drawing some pixels over the surface
        px_map = PixelArray(surface)

        # Each char in the map_str represents a rectangular area, which will have a certain size in pixels defined by
        # the surface x & y / map x & y
        rect_width = surface.get_width() / width
        rect_height = surface.get_width() / height

        for y in range(height):
            for x in range(width):
                if map_str[x + y * width] == ' ':
                    continue  # skip empty spaces

                # Work out top left corner x, y and the bottom right x, y
                rect_tl_x = int(x * rect_width)
                rect_tl_y = int(y * rect_height)
                rect_br_x = int(rect_tl_x + rect_width)
                rect_br_y = int(rect_tl_y + rect_height)

                # Draws a rectangle from x1:x2 and y1:y2
                px_map[rect_tl_x:rect_br_x, rect_tl_y:rect_br_y] = (0, 255, 255)

        px_map.close()
        return surface
