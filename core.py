import pygame

from images.level_image_generator import LevelImageGenerator
from map import Map


def main():
    win_w = 512
    win_h = 512

    map = "0000222222220000" \
          "1              0" \
          "1      11111   0" \
          "1     0        0" \
          "0     0  1110000" \
          "0     3        0" \
          "0   10000      0" \
          "0   0   11100  0" \
          "0   0   0      0" \
          "0   0   1  00000" \
          "0       1      0" \
          "2       1      0" \
          "0       0      0" \
          "0 0000000      0" \
          "0              0" \
          "0002222222200000"

    surface = LevelImageGenerator.generate(win_w, win_h)
    surface = Map.draw_on_surface(surface, map)
    pygame.image.save(surface, "out.bmp")


if __name__ == "__main__":
    main()
