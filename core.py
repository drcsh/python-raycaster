import math
import numpy as np
from timeit import default_timer as timer
import pygame

from engine.gamestate import GameState
from engine.utils.exceptions import GameExitException
from engine.player_objects.input_handler import InputHandler
from engine.level_objects.level import Level
from engine.player_objects.player import Player
from engine.raycaster import RayCaster


def main():
    dev_mode = False
    win_w = 512
    win_h = 512
    fov = math.pi / 3  # fov is expressed as a fraction of pi, i.e. a fraction of a 180 degree view (tau being 360)

    if dev_mode:
        win_w = win_w * 2

    map_str = "0000222222220000" \
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

    enemies = [
        {
            "x": 3.456,
            "y": 3.812,
            "tile": 2
        },
        {
            "x": 1.834,
            "y": 8.765,
            "tile": 0
        },
        {
            "x": 5.323,
            "y": 5.365,
            "tile": 1
        },
        {
            "x": 4.123,
            "y": 10.265,
            "tile": 2
        },
    ]

    # Pygame Setup
    pygame.init()
    pygame.key.set_repeat(100, 50)
    display_surface = pygame.display.set_mode([win_w, win_h])
    background_surface = pygame.Surface([win_w, win_h])

    # General Setup
    input_handler = InputHandler()

    # Game state
    level = Level.constructor(map_str, enemies)

    raycaster = RayCaster(display_surface, level, fov, dev_mode=dev_mode)

    player_x = 3.456
    player_y = 2.345
    player_a = 1.523
    player = Player(player_x, player_y, player_a, level)

    # Set up the GameState
    gamestate = GameState(player, level)

    clock = pygame.time.Clock()

    caster_ts = []
    caster_worst = -1
    caster_best = 10
    try:
        while True:
            input_handler.handle(player)

            for enemy in level.enemies:
                enemy.act(gamestate)

            start = timer()
            raycaster.cast(player.x, player.y, player.angle)
            raycaster.render_game_objects(player.x, player.y, player.angle)
            end = timer()

            caster_ts.append(end - start)

            pygame.display.flip()
            display_surface.blit(background_surface, (0, 0))

            if len(caster_ts) > 100:  # stop caster_ts becoming too long
                av = np.average(caster_ts)
                print(f"Caster avg cast time (last 100):{av}")
                if av > caster_worst:
                    caster_worst = av
                if av < caster_best:
                    caster_best = av
                caster_ts = []

            # cap the framerate
            clock.tick(60)

    except GameExitException as ex:
        print(f"Exiting: {ex}")
    except Exception as ex:
        print(f"Unexpected Error: {ex}")

    print(f"Caster avg cast time (last {len(caster_ts)}):{np.average(caster_ts)}")
    print(f"Caster best avg cast time for 100 renders: {caster_best}")
    print(f"Caster worst avg cast time for 100 renders: {caster_worst}")
    print(f"Depthmap dump: {raycaster.depth_map}")
    pygame.image.save(display_surface, "out.bmp")

    pygame.quit()


if __name__ == "__main__":
    main()
