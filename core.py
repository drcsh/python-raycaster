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
    game_map = Map(surface, map)

    player_x = 3.456
    player_y = 2.345
    player_a = 1.523
    game_map.draw_player(player_x, player_y)

    # Raycast a single ray!
    game_map.ray_cast(player_x, player_y, player_a)

    pygame.image.save(game_map.surface, "out.bmp")


if __name__ == "__main__":
    main()
