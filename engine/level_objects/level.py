import os

import pygame

from engine.utils import math_utils
from engine.game_objects.enemy import Enemy
from engine.level_objects.levelmap import LevelMap
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
            enemy_texturemap = TextureMap.load_from_file(os.path.join("textures", enemy_dict['texture_filename']))

            # Note that we don't need to do anything with the enemy object, it gets stored by the spirte_group
            enemy_obj = Enemy(
                sprite_group=enemies,
                x=enemy_dict["x"],
                y=enemy_dict["y"],
                texturemap=enemy_texturemap,  # Temp: Will replace with file name
                max_hp=50
            )  # TODO: hitpoints!

        return Level(level_map, enemies)

    def __init__(self, level_map, enemies):
        self.level_map = level_map
        self.enemies = enemies
        self.wall_textures = TextureMap.load_from_file(os.path.join("textures", "walls.png"))
        #self.enemy_textures = TextureMap.load_from_file(os.path.join("textures", "enemies.png"))

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

    def enemy_near_location(self, x, y, exclude_enemy=None):
        """
        Return an Enemy if there is one 'near' a given location. 'near' because enemies exist at a particular
        point in space, so we need to give a radius around them which they count as occupying.

        We use this both for players and enemies (to prevent enemies clipping each other). When checking for an enemy,
        pass the enemy itself in as the exclude_enemy to prevent it from blocking itself.

        :Todo: consider a refactor here. The exclude feels like a code smell.

        :param float x:
        :param float y:
        :param GameObj|None exclude_enemy: Exclude a specific enemy from the check
        :return:
        :rtype Enemy|None:
        """
        for enemy in self.enemies:
            if enemy == exclude_enemy:
                continue
            if math_utils.distance_formula(x, y, enemy.x, enemy.y) < 0.5:
                return enemy
