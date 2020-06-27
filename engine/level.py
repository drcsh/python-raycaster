import os

import pygame

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
                enemies,
                enemy_dict.get("x"),
                enemy_dict.get("y"),
                50
            )  # TODO: hitpoints!

        return Level(level_map, enemies)

    def __init__(self, level_map, enemies):
        self.level_map = level_map
        self.enemies = enemies
        self.wall_textures = TextureMap.load_from_file(os.path.join("textures", "walls.png"))
        self.enemy_textures = TextureMap.load_from_file(os.path.join("textures", "enemies.png"))

    def __del__(self):
        self.enemies.empty()
