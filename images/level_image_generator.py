from pygame import Surface, PixelArray


class LevelImageGenerator:

    @staticmethod
    def generate(width, height):
        """

        :param int width:
        :param int height:
        :return:
        """

        surface = Surface((width, height))
        px_map = PixelArray(surface)

        # This fills the image with R/G colour gradients
        for i in range(height):
            for j in range(width):
                r = 255 * i / float(height)
                g = 255 * j / float(width)
                b = 0
                px_map[i, j] = (r, g, b)

        px_map.close()
        return surface