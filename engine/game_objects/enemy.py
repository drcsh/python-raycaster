import math

import pygame

from engine.game_objects.game_object import GameObject
from engine.utils import math_utils


class Enemy(GameObject):
    """
    Enemy is a subclass of GameObject, in addition to the basic information tracked by GameObject, it keeps track of
    variables needed for the enemy, such as its HP.
    """

    DEFAULT_MOVE_SPEED = 0.25
    DEFAULT_ATTACK_RANGE = 0.5

    def __init__(self,
                 sprite_group,
                 x,
                 y,
                 max_hp,
                 texturemap_tile_num,
                 speed=DEFAULT_MOVE_SPEED,
                 attack_range=DEFAULT_ATTACK_RANGE):
        self.max_hp = max_hp
        self.hp = max_hp
        self.texturemap_tile_num = texturemap_tile_num  # Temp, for animation, each enemy will need their own TextureMap
        self.speed = speed
        self.attack_range = attack_range

        # This is used to throttle how many actions the enemy takes. E.g. we don't want an enemy to attack every single
        # game iteration, or it will attack as fast as the game runes.
        self.wait_until = 0

        super(Enemy, self).__init__(sprite_group, x, y, texturemap_tile_num)

    def act(self, gamestate):
        """
        This function defines the behavior of the enemy, it should be called once per game iteration.
        :return:
        """
        if pygame.time.get_ticks() < self.wait_until:
            return

        if self.has_los_to_player(gamestate):
            print("I SEE YOU!")
            self.move(gamestate)
            self.wait_until = pygame.time.get_ticks() + 500

    def has_los_to_player(self, gamestate):
        """
        This function determines if the enemy can see the player from where it is (i.e. if there is an uninterrupted
        line from the player to the enemy).

        :param gamestate:
        :return:
        """
        # TODO: will need to work this out similar to how the raycast works, by jumping along points of interest
        # absolute direction from the player_objects to the sprite (in radians)

        player_x = gamestate.player.x
        player_y = gamestate.player.y

        # Todo: this is lifted pretty much straight from Raycaster. Possible to rationalize?
        x_increasing = False
        y_increasing = False

        intercept = None  # y intercept, if this line is not vertical
        gradient = None  # gradient of this line

        # As long as this isn't a vertical line...
        if self.x != player_x:
            gradient = math_utils.gradient(self.x, self.y, player_x, player_y)

            x_increasing = player_x > self.x

            intercept = self.y - (gradient * self.x)

        # as long as this isn't a hotizontal line...
        if self.y != player_y:
            y_increasing = player_y > self.y

        ray_x = self.x
        ray_y = self.y

        ray_x_whole = ray_x % 1 == 0
        ray_y_whole = ray_y % 1 == 0

        while math_utils.distance_formula(ray_x, ray_y, player_x, player_y) > 1:

            x_poi_x, x_poi_y = math_utils.get_next_x_poi(player_x, ray_x, gradient, intercept, x_increasing,
                                                         ray_x_whole)
            y_poi_x, y_poi_y = math_utils.get_next_y_poi(player_x, player_y, ray_y, gradient, intercept, y_increasing,
                                                         ray_y_whole)
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

            map_symbol = gamestate.level.level_map.get_symbol_at_map_xy(plot_x, plot_y)

            if map_symbol != ' ':  # Wall in between player and enemy
                return False

        return True

    def move(self, gamestate):
        """
        Moves towards the player at self.speed until within attack range.
        
        :param GameState gamestate:
        :return:
        """

        if math_utils.distance_formula(self.x, self.y, gamestate.player.x, gamestate.player.y) < self.attack_range:
            return

        dir_to_player = math.atan2(gamestate.player.y - self.y, gamestate.player.x - self.x)

        cos_angle = math.cos(dir_to_player)
        sin_angle = math.sin(dir_to_player)

        self.x = self.x + self.speed * cos_angle
        self.y = self.y + self.speed * sin_angle

    def attack(self):
        # TODO: If the enemy can see the player and the enemy is in range, make an attack
        pass

    def take_damage(self, damage):
        """
        Basic version, remove the given damage from the hp count. If hp reaches 0, remove from the enemy list.

        TODO: Death animations etc.
        :param int damage:
        :return:
        """
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
