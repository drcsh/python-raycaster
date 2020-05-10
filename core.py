import math
import pygame

from images.level_image_generator import LevelImageGenerator
from map import Map
from raycaster import RayCaster


def main():
    win_w = 1024
    win_h = 512
    fov = math.pi / 3  # fov is expressed as a fraction of pi, i.e. a fraction of a total 360 circular view

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

    pygame.init()
    screen = pygame.display.set_mode([win_w, win_h])

    background = pygame.Surface((win_w, win_h))
    background.fill((255, 255, 255))
    game_map = Map(background, map)
    raycaster = RayCaster(win_w, win_h, fov)

    player_x = 3.456
    player_y = 2.345
    player_a = 1.523
    game_map.draw_player(player_x, player_y)

    # Raycast a single ray!
    raycaster.cast(game_map, player_x, player_y, player_a)

    screen.blit(game_map.surface, (0, 0))

    clock = pygame.time.Clock()
    running = True
    while running:
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(40)

        screen.blit(game_map.surface, (0, 0))
        pygame.display.flip()

    pygame.image.save(game_map.surface, "out.bmp")

    pygame.quit()


if __name__ == "__main__":
    main()
