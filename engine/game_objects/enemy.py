import math

import pygame

from textures.texturemap import TextureMap
from .animated_object import AnimatedObject
from engine.utils import math_utils
from ..gamestate import GameState


class Enemy(AnimatedObject):
    """
    Enemy is a subclass of AnimatedObject,  keeps track of variables needed for the enemies, such as HP.
    """

    DEFAULT_MOVE_SPEED = 0.25
    DEFAULT_ATTACK_RANGE = 1
    DEFAULT_ATTACK_DAMAGE = 20
    DAMAGE_DEALT_ON_STATE = 3

    def __init__(self,
                 sprite_group: pygame.sprite.Group,
                 x: float,
                 y: float,
                 max_hp: int,
                 texturemap: TextureMap,
                 speed: int = DEFAULT_MOVE_SPEED,
                 attack_range: float = DEFAULT_ATTACK_RANGE,
                 attack_damage: int = DEFAULT_ATTACK_DAMAGE):
        """
        :param sprite_group: Which spritegroup this will belong to
        :param x: X coord on the Map where this enemy appears.
        :param y: Y coord on the Map where this enemy appears.
        :param texturemap:
        :param max_hp:
        :param speed:
        :param attack_range:
        :param attack_damage:
        """

        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed
        self.attack_range = attack_range
        self.attack_damage = attack_damage

        # This is used to throttle how many actions the enemy takes. E.g. we don't want an enemy to attack every single
        # game iteration, or it will attack as fast as the game runes.
        self.wait_until = 0

        super().__init__(sprite_group, x, y, texturemap)

    @property
    def dead(self) -> bool:
        return self.hp <= 0

    def act(self, gamestate: GameState):
        """
        This function defines the behavior of the enemy, it should be called once per game iteration.
        :return:
        """
        if pygame.time.get_ticks() < self.wait_until:
            return

        if self.has_los_to_player(gamestate):

            if self.dead:
                self.die()
            elif self.can_attack(gamestate):
                self.attack(gamestate)
            else:
                self.move(gamestate)

            self.animate()
            self.wait_until = pygame.time.get_ticks() + self.ANIMATION_WAIT_TICKS

    def has_los_to_player(self, gamestate: GameState):
        """
        This function determines if the enemy can see the player from where it is (i.e. if there is an uninterrupted
        line from the player to the enemy).

        :param gamestate:
        :return:
        """

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

    def can_attack(self, gamestate: GameState):
        """
        Determines if the enemy is close enough to the player to attack
        """
        if math_utils.distance_formula(self.x, self.y, gamestate.player.x, gamestate.player.y) < self.attack_range:
            return True

        return False

    def move(self, gamestate: GameState):
        """
        Moves towards the player at self.speed until within attack range.
        """
        self.set_animation_type(self.MOVE_ANIMATION)

        dir_to_player = math.atan2(gamestate.player.y - self.y, gamestate.player.x - self.x)

        cos_angle = math.cos(dir_to_player)
        sin_angle = math.sin(dir_to_player)

        new_x = self.x + self.speed * cos_angle
        new_y = self.y + self.speed * sin_angle

        if self.check_location_valid(gamestate, new_x, new_y):
            self.x = new_x
            self.y = new_y

    def attack(self, gamestate: GameState):
        """
        Perform attack animation and do damage to the player.
        """
        self.set_animation_type(self.ATTACK_ANIMATION)

        # Don't deal the damage until the final frame of the attack animation
        if self.animation_state == self.DAMAGE_DEALT_ON_STATE:
            gamestate.player.take_damage(self.attack_damage)

    def die(self):
        """
        Perform the death animation and then remove the sprite.
        """
        self.set_animation_type(self.DEATH_ANIMATION)

        if self.animation_state == self.animation_state_max:
            self.kill()

    def take_damage(self, damage: int):
        """
        Reduce current HP by the damage taken until dead.
        """
        if not self.dead:
            self.hp -= damage
