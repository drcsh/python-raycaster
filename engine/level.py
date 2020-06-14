from pygame.sprite import Sprite

from engine.enemy import Enemy
from engine.levelmap import LevelMap


class Level:
    """
    Class for keeping track of an entire level, including the map and the enemies on it
    """

    @staticmethod
    def constructor(map_str, enemies_list):
        level_map = LevelMap(map_str)

        enemies = []
        for enemy_dict in enemies_list:

            sprite = Sprite([0, 0, 0], 200, 200)  # TODO: File loading
            enemy_obj = Enemy(enemy_dict.get("x"),
                              enemy_dict.get("y"),
                              sprite,
                              50)  # TODO: hitpoints!
            enemies.append(enemy_obj)

        return Level(level_map, enemies)

    def __init__(self, level_map, enemies):
        self.level_map = level_map
        self.enemies = enemies

