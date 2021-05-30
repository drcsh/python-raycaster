from typing import List, Optional

import pygame

from engine.game_objects.game_object import GameObject
from engine.utils import math_utils
from engine.game_objects.enemy import Enemy
from engine.level_objects.levelmap import LevelMap
from textures.texturemap import TextureMap


class Level:
    """
    Class for keeping track of an entire level, including the map and the enemies on it
    """

    @staticmethod
    def constructor(map_str: str, enemies_list: List[dict]):
        level_map = LevelMap(map_str)

        # Initialize Groups which will keep track of our sprites
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        for enemy_dict in enemies_list:
            enemy_texturemap = TextureMap.load_enemy(enemy_dict['texture_filename'])

            # Note that we don't need to do anything with the enemy object, it gets stored by the spirte_group
            enemy_obj = Enemy(
                sprite_group=enemies,
                x=enemy_dict["x"],
                y=enemy_dict["y"],
                texturemap=enemy_texturemap,  # Temp: Will replace with file name
                max_hp=50
            )  # TODO: hitpoints!

        return Level(level_map, enemies, bullets)

    def __init__(self, level_map: LevelMap, enemies: pygame.sprite.Group, bullets: pygame.sprite.Group):
        self.level_map = level_map
        self.enemies = enemies
        self.bullets = bullets
        self.wall_textures = TextureMap.load_from_file("walls.png")

    def __del__(self):
        self.enemies.empty()

    def wall_at_location(self, x: float, y: float) -> bool:
        """
        Return True/False for if there is a wall at a given location.
        """
        return self.level_map.get_symbol_at_map_xy(x, y) != ' '

    def enemy_near_location(self, x: float, y: float, exclude_enemy: Optional[GameObject] = None) -> Optional[Enemy]:
        """
        Return an Enemy if there is one 'near' a given location. 'near' because enemies exist at a particular
        point in space, so we need to give a radius around them which they count as occupying.

        We use this both for players and enemies (to prevent enemies clipping each other). When checking for an enemy,
        pass the enemy itself in as the exclude_enemy to prevent it from blocking itself.

        :Todo: consider a refactor here. The exclude feels like a code smell.

        exclude_enemy: Exclude a specific enemy from the check
        """
        for enemy in self.enemies:
            if enemy == exclude_enemy:
                continue
            if math_utils.distance_formula(x, y, enemy.x, enemy.y) < 0.5:
                return enemy

    def location_is_valid(self, x: float, y: float, exclude_enemy: Optional[GameObject] = None) -> bool:
        """
        Helper method for all (moving) game objects to determine if their new location is valid.

        :return: True if there's nothing blocking this location, False otherwise
        """
        if self.wall_at_location(x, y):
            return False

        if self.enemy_near_location(x, y, exclude_enemy=exclude_enemy):
            return False

        return True
    
    def line_of_sight_between_coords(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        """
        Works out if there is line of sight (LOS) between two points. E.g. if an enemy can see the player
        :return: 
        """
        # Todo: this is lifted pretty much straight from Raycaster. Possible to rationalize?
        x_increasing = False
        y_increasing = False

        intercept = None  # y intercept, if this line is not vertical
        gradient = None  # gradient of this line

        # As long as this isn't a vertical line...
        if x1 != x2:
            gradient = math_utils.gradient(x1, y1, x2, y2)

            x_increasing = x2 > x1

            intercept = y1 - (gradient * x1)

        # as long as this isn't a hotizontal line...
        if y1 != y2:
            y_increasing = y2 > y1

        ray_x = x1
        ray_y = y1

        ray_x_whole = ray_x % 1 == 0
        ray_y_whole = ray_y % 1 == 0

        while math_utils.distance_formula(ray_x, ray_y, x2, y2) > 1:

            x_poi_x, x_poi_y = math_utils.get_next_x_poi(x2, ray_x, gradient, intercept, x_increasing, ray_x_whole)
            y_poi_x, y_poi_y = math_utils.get_next_y_poi(x2, y2, ray_y, gradient, intercept, y_increasing, ray_y_whole)
            ray_x, ray_y = math_utils.get_closest_point(ray_x, ray_y, x_poi_x, x_poi_y, y_poi_x, y_poi_y)

            # the ray will be one of the identified POIs, so one of the x/y values will be whole
            ray_x_whole = ray_x == x_poi_x
            ray_y_whole = ray_y == y_poi_y

            plot_x = ray_x
            plot_y = ray_y
            if ray_x_whole and not x_increasing:
                plot_x = ray_x - 1

            if ray_y_whole and not y_increasing:
                plot_y = ray_y - 1

            map_symbol = self.level_map.get_symbol_at_map_xy(plot_x, plot_y)

            if map_symbol != ' ':  # Wall in between player and enemy
                return False

        return True
