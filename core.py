import os

import math
import numpy as np
from timeit import default_timer as timer
import pygame

from engine.map import Map
from engine.player import Player
from engine.raycaster import RayCaster
from textures.texturemap import TextureMapLoader


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
          "0 4444440      0" \
          "0              0" \
          "0002222222200000"

    pygame.init()
    screen = pygame.display.set_mode([win_w, win_h])

    wall_textures = TextureMapLoader.load_from_file(os.path.join("textures", "walls.png"))
    game_map = Map(win_w, win_h, map)

    raycaster = RayCaster(win_w, win_h, fov, wall_textures)

    player_x = 3.456
    player_y = 1.345
    player_a = 1.523
    player = Player(player_x, player_y, player_a)

    clock = pygame.time.Clock()
    running = True

    caster_ts = []
    while running:
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player.move_forward()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player.turn_left()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player.turn_right()
                break

        game_map.reset_surface()

        game_map.draw_player(player.x, player.y)

        start = timer()
        raycaster.cast(game_map, player.x, player.y, player.angle)
        end = timer()

        caster_ts.append(end - start)

        screen.blit(game_map.surface, (0, 0))
        pygame.display.flip()

        if len(caster_ts) > 100:  # stop caster_ts becoming too long
            print(f"Caster avg cast time (last 100):{np.average(caster_ts)}")
            caster_ts = []

        # cap the framerate
        clock.tick(60)

    print(f"Caster avg cast time (last {len(caster_ts)}):{np.average(caster_ts)}")
    pygame.image.save(game_map.surface, "out.bmp")

    pygame.quit()


if __name__ == "__main__":
    main()
