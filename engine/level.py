import os

import pygame

from engine import math_utils
from engine.enemy import Enemy
from engine.levelmap import LevelMap
from textures.texturemap import TextureMap


class Level:
    """
    Class for keeping track of an entire level, including the map and the enemies on it
    """

    @staticmethod
    def constructor(map_str, enemies_list):
        level_map = LevelMap(map_str)

        enemies = pygame.sprite.Group()
        for enemy_dict in enemies_list:
        
            enemy_obj = Enemy(
                sprite_group=enemies,
                loc_x=enemy_dict.get("x"),
                loc_y=enemy_dict.get("y"),
                texturemap_tile_num=enemy_dict.get("tile"),  # Temp: Will replace with file name
                max_hp=50
            )  # TODO: hitpoints!

        return Level(level_map, enemies)

    def __init__(self, level_map, enemies):
        self.level_map = level_map
        self.enemies = enemies
        self.wall_textures = TextureMap.load_from_file(os.path.join("textures", "walls.png"))
        self.enemy_textures = TextureMap.load_from_file(os.path.join("textures", "enemies.png"))

    def __del__(self):
        self.enemies.empty()

    def wall_at_location(self, x, y):
        """
        Return True/False for if there is a wall at a given location.
        :param float x:
        :param float y:
        :return:
        :rtype bool:
        """
        return self.level_map.get_symbol_at_map_xy(x, y) != ' '

    def enemy_near_location(self, x, y):
        """
        Return True/False if there is an enemy 'near' a given location. 'near' because enemies exist at a particular
        point in space, so we need to give a radius around them which they count as occupying.
        :param float x:
        :param float y:
        :return:
        :rtype bool:
        """
        for enemy in self.enemies:
            if math_utils.distance_formula(x, y, enemy.loc_x, enemy.loc_y) < 0.5:
                return True
